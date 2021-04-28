# 一些参见Dockerfile&docker-compose问题的解决

## Alpine

### 源替换
    在Dockerfile中加入一条：
    RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
    或清华源
    RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

### docker-compose中build的时候dns解析问题
    docker-compose.yml: 通过增加context以及network设置为host
        version: '3.4'
        services:
            kafka:
                build:
                    context: .
                    network: host
    其他方法：
        设置docker的dns等

