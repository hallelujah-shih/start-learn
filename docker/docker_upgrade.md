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

## reference
[docker升级](https://blog.docker.com/2015/07/new-apt-and-yum-repos/)

[docker安装](https://docs.docker.com/engine/installation/)
