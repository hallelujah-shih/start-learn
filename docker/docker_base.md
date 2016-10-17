# docker使用的一些基本准备事项

## 官方源替代为国内源
```
ubuntu:trusty为例子(替换为阿里的源)
apt源替换
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt-get update

pip源替换
RUN echo -e '[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\ntrusted = mirrors.aliyun.com' > .pip/pip.conf
```

## 设置ulimit core
```
1. core需要为-1，设置实际的数值无效
2. 由于需要在docker中更改/proc/sys/kernel/core_pattern文件，所以必须跟上--privileged参数
> docker run -it --ulimit core=-1 --privileged ubuntu:14.04 /bin/bash
3. 在docker中设置core文件的位置
> echo "core.%e.%p.%t" > /proc/sys/kernel/core_pattern
```

## reference
[docker core设置](http://ephrain.pixnet.net/blog/post/61630024-%5Bdocker%5D-%E5%9C%A8-container-%E8%A3%A1%E8%A8%AD%E5%AE%9A-core-dump-%E7%9A%84%E6%AA%94%E6%A1%88%E5%90%8D%E7%A8%B1)
