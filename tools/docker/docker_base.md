# docker使用的一些基本准备事项

## 官方源替代为国内源
```
ubuntu:trusty为例子(替换为阿里的源)
apt源替换
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt-get update

pip源替换
RUN echo -e '[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\ntrusted-host = mirrors.aliyun.com' > .pip/pip.conf
```

## 设置ulimit core
```
1. core需要为-1，设置实际的数值无效
2. 由于需要在docker中更改/proc/sys/kernel/core_pattern文件，所以必须跟上--privileged参数
> docker run -it --ulimit core=-1 --privileged ubuntu:14.04 /bin/bash
3. 在docker中设置core文件的位置
> echo "core.%e.%p.%t" > /proc/sys/kernel/core_pattern
```

## 数据管理
```
容器中管理数据主要由两种方式
1. 数据卷（Data Volumes）
2. 数据卷容器（Data Volume containers）
```

### 数据卷
```
特性：
1. 可以在容器之间共享和重用
2. 对数据卷的修改会马上生效
3. 对数据卷的更新不会影响镜像
4. 数据卷不会因为容器的删除而受到影响

命令：
-v

常用方法：
指定挂载本地主机的目录到容器中
> docker run -d -P --name web -v /src/webapp:/opt/webapp ubuntu:trusty /bin/bash
表示挂载主机上的/src/webapp目录到容器中的/opt/webapp目录，开发和测试十分方便
* 本地路径必须为绝对路径
Docker 挂载数据卷的默认权限是读写，用户也可以通过 :ro 指定为只读。
> docker run -d -P --name web -v /src/webapp:/opt/webapp:ro ubuntu:trusty /bin/bash
挂载为只读了

查看数据卷信息：
> docker inspect web
```

### 数据卷容器
```
如果你有一些持续更新的数据需要在容器间共享，最好创建数据卷容器
数据卷容器是正常的容器，专门用来提供数据卷，供其他容器挂载的

创建一个名为dbdata的数据卷容器
> sudo docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres 
其他容器中使用--volumes-from来挂载dbdata容器中的数据卷
> sudo docker run -d --volumes-from dbdata --name db1 training/postgres
> sudo docker run -d --volumes-from dbdata --name db2 training/postgres
```

## 镜像/容器的导入和导出
### 导出(save, export)
```
区别:
    save: 用于持久化镜像（不是容器），所以需要docker images查询镜像名来导出
        docker save busybox-1 > busybox-1.tar

    export: 用于持久化容器（不是镜像），所以需要docker ps -a得到容器ID
        docker export <container id> > export.tar
```

### 导入(load, import)
```
    load:
        docker load < busybox-1.tar

    import:
        cat export.tar | docker import - busybox-1-export:latest
```

### 区别
```
使用export-import方式处理的镜像会丢失所有历史
```

## Dockerfile一些命令介绍
```
一些指令介绍
```

### ADD和COPY
```

```

### ENTRYPOINT和CMD
```
都是在执行一条命令。在绝大多数情况下, 你只要在这2者之间选择一个调用就可以。 但他们有更高级的应用, CMD和ENTRYPOINT组合起来使用, 完成更加丰富的功能。

CMD可以直接被docker run跟上运行指令所覆盖
ENTRYPOINT的覆盖需要加上--entrypoint

所以，如果您希望执行一个具体程序，且不希望被执行docker run所随意覆盖，建议使用ENTRYPOINT
使用用例为test/print_args
cd test/print_args
docker build . -t print

"docker run print" 的输出如下：
2023/02/09 03:08:30 [/print -from-docker-file-cmd]

"docker run print -from-docker-run-cmd-replace" 的输出如下：
2023/02/09 03:09:55 [/print -from-docker-run-cmd-replace]

可以结合文档与测试得出，当组合时CMD是附在ENTRYPOINT后的。
```

## 杂项操作

### 停止自启动的镜像
```
查看正在运行容器的状态
docker inspect --format "{{ .HostConfig.RestartPolicy.Name }}" <CONTAINER_ID_or_NAME>

更新容器的自启动状态
docker update --restart=no <CONTAINER_ID_or_NAME>
```

## reference
[docker core设置](http://ephrain.pixnet.net/blog/post/61630024-%5Bdocker%5D-%E5%9C%A8-container-%E8%A3%A1%E8%A8%AD%E5%AE%9A-core-dump-%E7%9A%84%E6%AA%94%E6%A1%88%E5%90%8D%E7%A8%B1)
[docker practice](https://www.gitbook.com/book/yeasy/docker_practice/details)
