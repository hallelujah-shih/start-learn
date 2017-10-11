# 删除老旧内核(RedHat,CentOS)
## 列出现在使用内核版本
```
> uname -sr
Linux 3.10.0-693.2.2.el7.x86_64
```
## 列出所有在系统上安装了的内核版本
```
> rpm -q kernel
kernel-3.10.0-514.10.2.el7.x86_64
kernel-3.10.0-514.16.1.el7.x86_64
kernel-3.10.0-514.21.1.el7.x86_64
kernel-3.10.0-514.26.2.el7.x86_64
kernel-3.10.0-693.2.2.el7.x86_64
```
## 删除不用的内核
```
1. 安装yum-utils
2. 删除老旧内核
> package-cleanup --oldkernels --count=2
系统中将只会保留2个内核版本，其余的内核版本将会被清理
```
# 删除老旧内核(Fedora)
```
> dnf remove $(dnf repoquery --installonly --latest-limit 2 -q) 
同样是保留2个内核版本在系统中
也可以设置yum.conf中
installonly_limit=2 #set kernel count
下次执行update的时候自动只保留2个内核版本
```
