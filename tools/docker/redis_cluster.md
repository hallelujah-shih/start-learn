# redis-cluster
```
> git clone https://github.com/itsmetommy/docker-redis-cluster.git

> cd docker-redis-cluster
> docker-compose up --build -d
# 查看容器
> docker ps
# 查看redis-1日志
> docker-compose logs redis-1
# 创建集群
> docker exec -it redis-1 redis-cli -p 7000 --cluster create 10.0.0.2:7000 10.0.0.3:7001 \
10.0.0.4:7002 10.0.0.5:7003 10.0.0.6:7004 10.0.0.7:7005 \
--cluster-replicas 1
# 查看node
> cluster nodes
# 查看slots
> cluster slots

```
