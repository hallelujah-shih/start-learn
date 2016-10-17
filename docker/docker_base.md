# docker使用的一些基本准备事项

## 官方源替代为国内源
```
ubuntu:trusty为例子(替换为阿里的源)
apt源替换
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt-get update

pip源替换
RUN echo -e '[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\ntrusted = mirrors.aliyun.com' > .pip/pip.conf
```
