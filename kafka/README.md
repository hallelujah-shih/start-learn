# KAFKA集群升级和扩展
```
由于kafka也是软件，也有bug要修复，有的bug重要，比如资源泄露，还有会有新的特性的加入等，所以需要升级
而扩展而言，由于业务的增长以及可靠性要求等，也需要根据需求调整topic
```

## KAFKA集群升级
```
升级过程（0.8.2.1->0.9.0.1）：
1. 检查跨版本升级是否存在一些配置上的变动
2. 在kafka_0.9的配置文件中加入inter.broker.protocol.version=0.8.2.1，停止原有的kafka_0.8的服务并启动kafka_0.9的服务
3. 重复2，将集群中所有kafka服务全部升级
4. 全部服务升级完成后，将inter.broker.protocol.version=0.9.0.0，并重启集群中所有服务，升级完成
```

## KAFKA集群扩展
```
给现有kafka集群增加物理机
1. 和现有集群中的kafka配置保持一致（broker.id不要重复）
2. 调整topic信息，将topic的partition重新分配，便于利用新加入集群的机器

修改partition个数: kafka-topics.sh --alter --topic <topic_name> --partitions <new_partition_num.> --zookeeper <zk_cluster>
调整partition分布: kafka-reassign-partitions.sh --zookeeper <zk_cluster>> --reassignment-json-file <rebalance_json_file> --execute

reassignment-json-file:
{
    "version": 1,
    "partitions": [
        {"topic": "hello1", "partition": 0, "replicas": [1, 2, 3]},
        {"topic": "world1", "partition": 0, "replicas": [1, 2, 3]},    
        {"topic": "world1", "partition": 1, "replicas": [2, 3, 1]},    
        {"topic": "world1", "partition": 2, "replicas": [3, 1, 2]} 
    ]
}
```

## 引用
[kafka滚动升级](http://kafka.apache.org/090/documentation.html#upgrade)
[kafka滚动升级注意事项](http://kafka.apache.org/090/documentation.html#upgrade_9_breaking)
[rebalance topics in a kafka cluster](https://blog.imaginea.com/how-to-rebalance-topics-in-kafka-cluster/)
