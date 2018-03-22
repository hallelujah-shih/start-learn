# ETCD相关问题汇总

## 安装
```
这里只做静态配置说明，且证书在保证安全的情况下，可以简化为peer cert, client cert，证书创建过程省略，可以参见cfssl的操作
关键配置字段列表
	name: 集群内唯一的名字
	data-dir
	listen-peer-urls:
	listen-client-urls:
	initial-advertise-peer-urls: 集群节点之间通信地址
	advertise-client-urls: 对外暴露的服务地址（客户端访问地址）
	initial-cluster: 集群列表的地址（每次etcdctl member命令修改以后记得在此处修改下，便于统一和查看）
	initial-cluster-token: 集群的token
	initial-cluster-state: 第一次初始化都是new，后续是existing
	client-transport-security: 配置证书信息
	peer-transport-security: 配置节点间通信的证书信息
```

## 调优
```
默认配置适合网络延迟较低的本地网络，当etcd服务跨多个数据中心的时候可能高延迟，需要调整相关配置
```

### 时间参数
```
heartbeat-interval：心跳间隔时间，单位为毫秒，通常是RTT的0.5-1.5X之间，太小会增加网络和CPU负担
election-timeout: follower节点在不会听到心跳的超时时间，并尝试成为leader节点，此值至少为RTT的10倍，此值的上限为50s
```

### 磁盘
```
etcd集群对磁盘的低延迟非常敏感，可以通过ionice调整
> sudo ionice -c2 -n0 -p `pgrep etcd`
```

### 网络
```
当leader服务于大量并发客户端请求，可能会延迟处理follower的请求，导致网络拥塞，在follower节点上表现为类似如下消息:
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
若遇上了，参见官网上的处理方案
```

## 监控
```
现在官方推荐为普罗米修斯
```

## 可视化管理
```
github.com/soyking/e3w
```

## 访问控制
```
*此处只操作V3，访问控制的V2与V3不同

特殊用户(root)和特殊规则(root)
user: root用户有所有的访问权限，必须在激活认证前创建此用户
role: root角色可以授予除了root用户以外的所有用户。root角色一般授予常规的集群维护，包括更新集群的关系，碎片整理以及创建快照。
```

### 用户，角色
```
创建用户
> etcdctl user add lvs
创建角色
> etcdctl role add lvs_role

给指定某个key设置读权限
> etcdctl role grant-permission lvs_role read /foo
给指定前缀的keys设置读权限(/bar/.)
> etcdctl role grant-permission lvs_role --prefix=true read /bar/
给指定key设置写权限(/aaa/bbbb)
> etcdctl role grant-permission lvs_role write /aaa/bbbb
给指定范围的keys赋予读写权限([key1, key5))
> etcdctl role grant-permission lvs_role readwrite key1 key5
给予某前缀完整的访问权限(/pub/.)
> etcdctl role grant-permission lvs_role readwrite --prefix=true /pub/

给某用户发放角色
> etcdctl user grant-role lvs lvs_role

> etcdctl user add root
> etcdctl auth enable
```


## FAQ

### 如何将单节点改为集群
```
1. 改变单节点模式为单节点集群模式
	需要将force-new-cluster改为true
	此处示例关键配置如下:
	name: node01
	data-dir: /dir/for/data-dir
	listen-peer-urls: http://192.168.1.1:2480,http://127.0.0.1:2480
	listen-client-urls: http://192.168.1.1:2479,http://127.0.0.1:2479
	initial-advertise-peer-urls: http://192.168.1.1:2480
	advertise-client-urls: http://192.168.1.1:2479
	initial-cluster: node01=http://192.168.1.1:2480
	initial-cluster-token: 'you_token'
	initial-cluster-state: existing
	force-new-cluster: true
	并启动单节点集群

2. 查看集群列表和状态
	> ./etcdctl --endpoint http://localhost:2479 member list
	* 注意，需要检查输出列表中的peerURLs，看是否和自己节点配置的initial-advertise-peer-urls值是否一致，我这儿不一致，需要先更新整个集群的信息
	> ./etcdctl --endpoint http://localhost:2479 member update $you_node_id http://192.168.1.1:2480
	记得先修改config信息，特别注意，一定要将force-new-cluster改为false(避免操作过程中意外服务重启或者忘记了)

3. 集群增加节点操作
	a. 先通过etcdctl member add需要加入的节点信息
	b. 上述命令会输出ETCD_NAME,ETCD_INITIAL_CLUSTER,ETCD_INITIAL_CLUSTER_STATE，在新节点创建的时候配置相应的值即可
		其中本地节点的配置initial-cluster的值需要更新
	> ./etcdctl --endpoint http://localhost:2479 member add node03 http://192.168.1.3:2480
	* 注意不管怎么操作，记得将所有节点的initial-cluster保持一致，便于查看

4. 查看集群状态
	> ./etcdctl --endpoint http://localhost:2479 cluster-health -f
```

### 在现有集群上开启https
```
1. 安装cfssl并生成证书
	> go get -u -v github.com/cloudflare/cfssl/cmd/...
	> mkdir ~/cfssl
	> cd ~/cfssl
	> cfssl print-defaults config > ca-config.json
	> cfssl print-defaults csr > ca-csr.json
	对ca-config.json以及ca-csr.json的修改参见本地文件

	创建CA
	> cfssl gencert -initca ca-csr.json | cfssljson -bare ca -

	创建server证书，最重要的是Common Name(CN)和hosts
	> cfssl print-defaults csr > server.json
	我示例中没有域名，直接是IP，server.json内容如下:
	{
		"CN": "server",
		"hosts": [
			"127.0.0.1",
			"192.168.1.1",
			"192.168.1.2",
			"192.168.1.3"
		],
		"key": {
			"algo": "ecdsa",
			"size": 256
		},
		"names": [
			{
				"C": "US",
				"ST": "CA",
				"L": "San Francisco"
			}
		]
	}
	上面的示例要注意的是algo选择，若选择ecdsa，在调用grpc的时候一定要确认GRPC_SSL_CIPHER_SUITES中有ecdsa套件的，如：ECDHE-ECDSA-AES256-GCM-SHA384，
	python-etcd3的库在使用的时候就需要先设置环境变量；若algo使用rsa，需要将size至少设置为2048
	> cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server server.json | cfssljson -bare server

	创建各个节点所用证书
	> cfssl print-defaults csr > node01.json
	内容示例如下
	{
		"CN": "node01",
		"hosts": [
			"127.0.0.1",
			"192.168.1.1",
			"192.168.1.2",
			"192.168.1.3"
		],
		"key": {
		"algo": "ecdsa",
		"size": 256
		},
		"names": [
			{
				"C": "US",
				"ST": "CA",
				"L": "San Francisco"
			}
		]
	}
	> cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=peer node01.json | cfssljson -bare node01
	分别创建另外几个节点的证书

	创建客户端证书
	> cfssl print-defaults csr > client.json
	关键字段如下配置：
	...
		"CN": "client",
		"hosts": [""],
	...
	> cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client client.json | cfssljson -bare client

2.  在现有集群上配置HTTPS
	a. copy上面为每个node生成的证书key以及ca证书到某个能访问的目录，这儿用的是/etc/ssl/etcd
	b. 分别为每台机器配置证书信息,并重启服务
		示例:
		client-transport-security:
			ca-file： /etc/ssl/etcd/ca.pem
			cert-file: /etc/ssl/etcd/node00.pem
			key-file: /etc/ssl/etcd/node00-key.pem
			client-cert-auth: true
			trusted-ca-file: /etc/ssl/etcd/ca.pem
		peer-transport-security:
			ca-file: /etc/ssl/etcd/ca.pem
			cert-file: /etc/ssl/etcd/node00.pem
			key-file: /etc/ssl/etcd/node00-key.pem
			peer-client-cert-auth: true
			trusted-ca-file: /etc/ssl/etcd/ca.pem
	c. 改变etcd的peer urls
		> etcdctl member list | awk -F'[: =]' '{print "etcdctl member update "$1" https:"$7":"$8}'
		执行输出结果，更改peer urls
	d. 改变etcd的client配置
		listen-client-urls，advertise-client-urls改为https
		listen-peer-urls改为https
	e. 重启所有节点的服务，并测试是否正确
		> etcdctl --endpoint https://127.0.0.1:2479 --ca-file ~/ca.pem --cert-file ~/client.pem --key-file ~/client-key.pem cluster-health -f
```
