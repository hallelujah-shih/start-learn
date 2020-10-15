# docker升级
```
以ubuntu 14.04为例
```

## 准备工作
```
ubuntu 14.04/15.10/16.04需要安装linux-image-extra-*内核包，允许你用aufs
> apt-get update
> apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual

增加key
> apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

编辑/etc/apt/sources.list.d/docker.list

deb https://apt.dockerproject.org/repo ubuntu-trusty main
```

## 升级
```
删除老的
apt-get purge lxc-docker*

安装新的
apt-get install docker-engine
```

## 配置内部使用的可信源
### ubuntu 14.04
```
编辑/etc/default/docker

添加以下内容：
DOCKER_OPTS="$DOCKER_OPTS  --registry-mirror=https://registry.aliyuncs.com --insecure-registry=test-cdn-chengdu-office5:5000"
service docker restart

docker login test-cdn-chengdu-office5:5000
    username
    passwd
```
### CentOS 7
```
现在(2016.12.20)docker启动名字为dockerd
编辑/lib/systemd/system/docker.service文件的ExecStart行，在其后增加内容如下：
 --registry-mirror=https://registry.aliyuncs.com --insecure-registry=test-cdn-chengdu-office5:5000
由于服务文件已经改变，执行
$ systemctl daemon-reload 
$ systemctl restart docker.service
$ docker login test-cdn-chengdu-office5:5000
username
passwd 即可工作
```

## reference
[docker升级](https://blog.docker.com/2015/07/new-apt-and-yum-repos/)

[docker安装](https://docs.docker.com/engine/installation/)

[docker镜像加速](https://yq.aliyun.com/articles/29941)
