# netfilter
```
一些netfilter相关学习记录
iptables工具的模块目录 /lib64/xtables
netfilter对应的模块目录/lib/modules/`uname -r`/net/netfilter
```

## netfilter命令结构
```
netfilter被分为4个表：filter，nat，mangle，raw
```
### filter
```
filter是netfilter中最重要的机制，任务是执行数据包的过滤操作（防火墙）
有三个链，分别是INPUT、FORWARD、OUTPUT
```

### nat
```

```
### mangle
```
允许通过mangle机制来修改经过防火墙内数据包的内容
```

### raw
```
负责加快数据包穿过防火墙机制的速度，提高防火墙性能
```

## iptables工具的使用方法
```
iptables的命令结构为
iptables -t $TABLE -$OP $rule
如filter表的操作方式有
-L 列出表内容
-F 清除表内容
-A 加入新规则
-P 设置默认策略
-I 插入新规则
-R 取代规则
-D 删除规则
```
### iptables规则语法
```
!表示非逻辑
-p protocol 用于匹配某种特定协议（all 匹配任何协议，参考/etc/protocols）

-s source 匹配源IP（可以是单一IP或CIDR网段；FQDN是iptables工具将FQDN送到DNS解析为IP的）
-d destination 匹配目的IP
--sport source port
--dport dst port
--src-range
--dst-range

-i in-interface 匹配数据包的进出接口
-o out-interface

-m
 state
 multiport
 iprange
 owner
 ttl
 limit
 connlimit

-j jump 将复合条件的数据包用特定方式处理（ACCEPT，DROP，REJECT）
ex: 不允许192.168.0.200主机通过本机DNS服务执行解析 iptables -A INPUT -p udp -s 192.168.0.200 --dport 53 -j REJECT

ex: 每分钟允许进入的ICMP包数量是10个，如果超过了10个，那么限制每分钟只能进来6个ICMP包
    iptables -A INPUT -p icmp --icmp-type 8 -m limit --limit 6/m --limit-burst 10 -j ACCEPT # --limit-burst 10表示每分钟进入10个包 -j ACCEPT表示允许的，即如果每分钟进入的ICMP包数小于10个，是被允许的，超过10个，就限制每分钟只能进入6个
    iptables -A INPUT -p icmp --icmp-type 8 -j DROP # 上面规则没有被允许的则在此处丢弃

** 注意 ** 涉及 --sport --dport参数，一定要指定TCP或UDP协议
```

## 模块介绍
### state模块
```
四种状态:
ESTABLISHED: 只要数据包能成功穿过防火墙之后所有数据包（包括反向所有数据包），其状态都为ESTABLISHED
NEW：连接的第一个报文的状态都是NEW
RELATED：指被动产生的应答数据包，而且这个数据包不属于现有任何的连接，且与协议无关，只要应答的数据包是因为本机先送出一个数据包而导致另一条连接的产生，那么这个新连接的所有数据包都属于RELATED状态的数据包。

INVALID：是不属于NEW ESTABLISHED RELATED状态的数据包。
```

### hashlimit模块
```
参数列表:
--hashlimit-upto 如果速率低于或等于此值，则匹配
--hashlimit-above 如果速率高于此值，则匹配
--hashlimit-burst 允许突发的个数(其实就是令牌桶最大容量)。默认为 5。
--hashlimit-mode {srcip|srcport|dstip|dstport},…*
--hashlimit-srcmask 当mode设置为srcip时, 配置相应的掩码表示一个网段。
--hashlimit-dstmask 当mode设置为dstip时, 配置相应的掩码表示一个网段。
--hashlimit-name 
--hashlimit-htable-size 散列表的桶数（buckets）。
--hashlimit-htable-max 散列中的最大条目。
--hashlimit-htable-expire hash规则失效时间, 单位毫秒(milliseconds)。
--hashlimit-htable-gcinterval 垃圾回收器回收的间隔时间, 单位毫秒。

ex: hashlimit-upto
iptables -A OUTPUT -p icmp -m hashlimit --hashlimit-name icmp --hashlimit-upto 5/s --hashlimit-burst 10 -j ACCEPT
iptables -A OUTPUT -p icmp -j DROP

ex: hashlimit-above
iptables -A OUTPUT -p icmp -m hashlimit --hashlimit-name icmp --hashlimit-above 5/s --hashlimit-burst 10 -j DROP
```

## netfilter的NAT机制
```
变更source ip的机制叫SNAT
变更dest ip的机制叫DNAT

pub_addr: 10.0.1.200
web: 192.168.0.1 port: 80, 443
mail: 192.168.0.2 port: 25, 110

web服务器
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to 192.168.0.1:80
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to 192.168.0.1:443

mail服务器
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 25 -j DNAT --to 192.168.0.2:25
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 110 -j DNAT --to 192.168.0.2:110

iptables -t nat -A POSTROUTING -o eth0 -s 192.168.0.0/24 -j SNAT --to 10.0.1.200
```

## netfilter的Mangle机制
```
Mangle机制可用于修改数据包内容
 如：修改IP包头的TTL
```

## netfilter的raw机制
```
```

## 处理方法
### ACCEPT&DROP
```
ACCEPT&DROP是最基本的方法
```
### QUEUE
```
QUEUE是将符合条件的数据包转发给User space的应用程序来处理。
ex: iptables -A FORWARD -p tcp -d $MAIL_SERVER --dport 25 -j QUEUE
```
### RETURN
```
RETURN是用在用户定义的链中，目的是让符合规则的数据包提前返回其原来的链。

用户可以任意扩充新链(User Define Chain)
 * 添加
    iptables -N WEB_SRV #添加名为WEB_SRV的新链
 * 删除
    iptables -X WEB_SRV # 删除前必须先清除链内规则
 * 修改
    iptables -E OLD_NAME NEW_NAME

数据包经过netfilter结构时，默认不会进入任何用户定义的链中，必须让用户定义的链与INPUT链产生关联的关系。
```
### REJECT
```
REJECT是由ipt_REJECT.ko模块提供的功能。与DROP类似，但是会发送中断应答报文

```
### LOG
```
LOG由ipt_LOG.ko提供的功能,用于产生日志
```


## netfilter连接处理能力与内存消耗
```
/proc/sys/net/netfilter/nf_conntrack_max文件限制了nf_conntrack模块所能跟踪的最大连接数；简单计算方式为CONNTRACK_MAX=RAMSIZE(in_bytes)/16384/（x/32)其中x是操作系统的地址位数；如32位系统，512M内存nf_conntrack_max默认为:512*1024*1024/16384=32768

假设nf_conntrack是内核模块形式存在，且需要跟踪连接数量为262144，参考hashsize为:262144/8=32768，并先移除nf_conntrack模块
再重新加载: modprobe nf_conntrack hashsize=32768

跟踪一条简单连接会消耗276字节空间(如普通TCP连接)，262144*276/1024/1024 = 69M(不同版本的nf_conntrack所需空间不一定相同)

* 只要系统有载入nf_conntrack模块，任何穿过防火墙的连接都会被记录在/proc/net/nf_conntrack(为啥我系统上没看到？)
* 若不想nf_conntrack跟踪连接，可以通过raw表
```

