# ES集群监控
## 期望
1. 集群的健康监控和数据可用性监控
2. 节点的错误监控
3. ES的缓存大小监控
4. 系统的使用情况（CPU，内存，磁盘）监控
5. 查询响应时间监控
6. 查询的频率监控
7. 数据入index的时间监控
8. 数据入index的速率
9. index和shard的数量监控
10. index和shard的空间大小监控
11. 系统配置监控

## 工具
1. Elasticsearch-head
2. Bigdesk
3. Marvel
4. Kopf
5. Kibana

## 安装和配置ES
```
以Ubuntu为例

安装ES，略

配置ES集群(下面两个路径是如果用apt套件安装的ES之后)
配置文件路径 /etc/elasticsearch/elasticsearch.yaml
环境变量的配置路径 /etc/default/elasticsearch

基本配置
cluster.name 你准备使用的集群的名字
ES_HEAP_SIZE=8g (设置为可用内存的一半，且不要超过30.5G)
ulimit -n 确定能打开的文件数，默认1024太小，需要自己调整 ES测试（curl -XGET 'http://10.8.255.182:9200/_nodes?os=true&process=true&pretty=true'） 
" *表示所有用户，你可以为ES单独创建用户，懒点即可，记得sshd_config -> UsePAM yes & service ssh restart
* soft nofile 65536
* hard nofile 65536

注意，如果没有生效，检查/etc/pam.d/common-session中，加入session required pam_limits.so
我的配置如下:
/etc/security/limits.conf
app             hard     nofile          65536
app             soft     nofile          65536
app             hard     memlock         unlimited
app             soft     memlock         unlimited

/etc/pam.d/common-session
session required pam_limits.so

swapoff -a (关闭所有swap分区，永久的需要在/etc/fstab -> /dev/xxxxx none swap sw 0 0关闭交换空间这部分非常重要，ES使用这个会对性能产生影响;由于关闭swap分区会对所有系统程序产生作用，可以只限制ES程序,1. 设置ES_HEAP_SIZE, 2. 设置MAX_LOCKED_MEMORY=unlimited 3. bootstrap.mlockall: true 4. service elasticsearch restart)
node.name  mynode-1 配置你的节点名

如果不是集群默认的都可以
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.unicast.hosts: ["mynode-2", "mynode-3"]
index.routing.allocation.disable_allocation: false
cluster.routing.allocation.enable : all 具体细节可以看(https://www.elastic.co/guide/en/elasticsearch/reference/current/shards-allocation.html#shards-allocation)


注意，必须保证:
1. ES的heap size为1/2的可用系统内存，但是不要超过31GB（边际效应）
2. 关闭内存交换分区
3. 锁定物理内存, bootstrap.mlockall: true

fielddata cache的配置
此配置设置不当，往往是引发OutOfMemoryError的根源(当执行sort或aggregation或facet查询，ES会从查询结果的不同字段填充到缓存；这使得相似的查询或子查询等执行得更快。默认情况ES不会设置缓存上限，所以缓存数据不会自动的清理，如果缓存引起了总的JVM内存达到或者超过ES_HEAP_SIZE，这个节点就会抛出OutOfMemoryError，从而要求ES节点重启)
indices.fielddata.cache.size: 30%  #限制fielddata cache的大小为可用JVM heap size的30%
如果节点上发现是因为fielddata cache引起的溢出，需要设置这个选项，但是这个选项会影响查询速度，因为需要重新填充缓存，再做查询(如果在节点上发现了此异常，可以在bigdesk或marvel中查看cache size是否正常，以此来判断是否需要设置此选项)
indices.fielddata.cache.expire 不要动此选项，不会影响查询性能
即使设置了fielddata.cache也可能出现单个查询产生OutOfMemoryError的情况，比如fielddata cache设置的2GB，但是我们单个查询，尝试加载2.5GB的数据到cache中，就出现了
indices.breaker.fielddata.limit: 60%
设置了之后，如果单个查询的fielddata超过了heap的60%，就会产生“熔断”，产生查询异常，而不是OutOfMemoryError(产生查询异常优于OutOfMemoryError)

分析查询(query操作，fetch操作，index操作)
query:查找操作
index.search.slowlog.threshold.query.warn: 8s
index.search.slowlog.threshold.query.info: 4s
index.search.slowlog.threshold.query.debug: 2s
index.search.slowlog.threshold.query.trace: 500ms

fetch:从index中获取感兴趣的文档
index.search.slowlog.threshold.fetch.warn: 1s
index.search.slowlog.threshold.fetch.info: 750ms
index.search.slowlog.threshold.fetch.debug: 500ms
index.search.slowlog.threshold.fetch.trace: 250ms

index:新文档在ES中做索引
index.indexing.slowlog.threshold.index.warn: 8s
index.indexing.slowlog.threshold.index.info: 4s
index.indexing.slowlog.threshold.index.debug: 2s
index.indexing.slowlog.threshold.index.trace: 500ms

index.indexing.slowlog.level: info
index.indexing.slowlog.source: 5000
最后在/path/to/es_log/*_cluster_*_slowlog.log*中查看日志
```


## 工具安装
### 安装配置Elasticsearch-head（只需要安装到一个节点即可）
```
> /path/elasticsearch/bin/plugin install mobz/Elasticsearch-head
or
> /path/elasticsearch/bin/plugin install file:///path/to/Elasticsearch-head.zip

service elasticsearch restart

http://path:port/_plugin/head/
```

### 安装配置Bigdesk（只需要安装到一个节点即可）
```
> /path/elasticsearch/bin/plugin install AIsaac08/bigdesk
or
> /path/elasticsearch/bin/plugin install file:///path/to/bigdesk.zip

service elasticsearch restart
访问 http://10.8.255.182:9200/_plugin/bigdesk/#nodes
```

### 安装配置Marvel（这个非常强大，好像5.x后就是elastic stack的标准监控了?）
```
Marvel分为两部分
1. Marvel Agent(依赖于Marvel License)
2. Marvel Dashboard(依赖于Kibana)

安装Marvel Agent:
> /path/elasticsearch/bin/plugin install license
> /path/elasticsearch/bin/plugin install marvel-agent
or
> /path/elasticsearch/bin/plugin install file:///path/to/license.zip
> /path/elasticsearch/bin/plugin install file:///path/to/marvel-agent.zip

安装Marvel(路径我乱写的，根据实际路径正确填写):
    安装kibana
    > wget https://download.shit.org/kibana.tar.gz
    > tar xzvf kibana.tar.gz

    > wget https://download.elasticsearch.org/elasticsearch/marvel/marvel-2.3.3.tar.gz
    > ./kibana/bin/kibana plugin --install marvel --url file:///tmp/marvel-2.3.3.tar.gz

    > ./kibana/bin/kibana
    这样安装的marvel会将数据产生在主集群中，可以配置marvel数据存储和主集群分开

分离版marvel dashboard配置
    存储marvel数据的es配置
      index.routing.allocation.disable_allocation: false
      cluster.routing.allocation.enable : al
      marvel.agent.enabled: false
      cluster.name: my_monitoring_cluster
      node.name: elasticsearch-marvel-01
      bootstrap.mlockall: true
      discovery.zen.ping.multicast.enabled: false
    并在此ES机器上安装Elasticsearch-head，参见此插件的安装

    并在主集群每台机器上安装marvel-agent(过程见前面，license, marvel-agent)
    在每台主集群机器上elasticsearch.yml中加入如下信息
    marvel.agent.exporters:
      my_monitoring_cluster:
        type: http
        host: ["http://elasticsearch-marvel-01:9200", "http://shit00:9200", "http://shit01:9200"] # 此处填写你kibana需要读取数据的地方，并在kibana的配置中配置正确
    marvel比较完整的配置信息如下:
    marvel.agent.exporters:
      my_monitoring_cluster:
        type: http
        host: ["host_list"]
        auth:
          username: basic_auth_username # 可选
          password: basic_auth_passwd # 可选
        connection:
          timeout: 6s # 可选，连接超时
          read_timeout: 60s # 可选，应答超时
          keep_alive: true
        ssl:
          hostname_verification: true
          protocol: TLSv1.2
          truststore.path: /path/to/file
        .jks truststore
          truststore.password: password
          truststore.algorithm: SunX509
        index:
          name:
            time_format: YYYY.MM.dd

    在elasticsearch-marvel-01安装marvel(不是marvel-agent)
    安装kibana，正确配置es的url如：elasticsearch.url: http://elasticsearch-marvel-01:9200
    最后启动kibana，并访问http://elasticsearch-marvel-01:5601/app/marvel
```

### 安装配置kopf(只需要在一个节点上安装)
```
es version              kopf branch
0.90.x                  0.90
1.x                     1.0
2.x                     2.0

> ./elasticsearch/bin/plugin install lmenezes/elasticsearch-kopf/{branch}
我机器上安装如下
> bin/plugin install lmenezes/elasticsearch-kopf/2.0

打开
http://es-node:9200/_plugin/kopf
```

## 问题和性能解决
### OutOfMemoryError
```
详情可以见配置中的fielddata cache相关的描述
```
### 记录查询、获取数据、入索引慢的问题
```
详细配置见ES配置中的slowlog相关配置，用于找到问题所在
```
### 解决查询性能问题
```
High-cardinality字段（cardinality在数据库领域的词）
如，时间精度到毫秒的查询，会很快将fielddata cache填满，而引发OutOfMemoryError，一个好的办法是使用低精度的时间进行存储和查询。

查询一个小的index的集合
当ES的索引个数增长后，查询将会遇到性能问题。解决这一问题的方案就是使用小的index集合做查询(非常适合现有索引查询的优化，现在的索引以时间为index)

冷索引（Cold indices）
产生原因
1. 新的数据被索引
2. 自动的分片移动和平衡
3. ES节点重启
4. cache被手动清除了
关于warmer index相关的：
https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-warmers.html
https://www.elastic.co/guide/en/elasticsearch/guide/current/preload-fielddata.html

分片的查询缓存(这个默认是关闭的，和fielddata cache不一样，最好使用前看是否能用上再决定是否打开)
indices.cache.query.size: 2%
https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html
```

### 系统和数据的架构
#### Hot-Warm架构
```
现有的日志数据可以考虑这种架构，较为适合
https://www.elastic.co/blog/hot-warm-architecture

配置热点节点
node.box_type: hot

配置温数据节点
node.box_bype: warm

```
##### master节点
```
理想情况，专用3节点作为master nodes,不存储数据，不做查询。这些机器不需要多强大，只是用于管理节点所用
```
##### Hot-data节点
```
这些节点上保存最频繁操作的数据索引，所有数据直接写到这些机器上，这些机器需要由良好的I/O，因为还可能是最频繁的查询节点，最好用SSD或者RAID 0
```
##### Warm-data节点
```
不会写数据到这些节点中，但是里面包含了历史数据
```

#### 降低磁盘使用
```
数据压缩（>= ES-2.0）
引入问题：会使得索引新的数据变得更慢

可以在Hot-Warm架构中使用，并增加Warm节点的压缩级别
1. 关闭索引
2. 配置index.codec为best_compression
3. 重新打开索引
curl -XPOST /index_name/_close
curl -XPOST /index_name/_settings -d '{"settings": {"index.codec": "best_compression"}}'
curl -XPOST /index_name/_open
```
#### 优化数据摄入
```
1. 批量入数据(bulk)，可以在marvel上看入数据的速度和频率
2. 磁盘配置为RAID 0，数据可靠性由ES保证(SSD更好)
```

