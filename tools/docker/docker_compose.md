# docker compose的简单使用
```
compose是面向项目进行管理的，而一个项目可以由多个服务（容器）关联而成
```

## 安装
```
> pip install -U docker-compose
> docker-compose -h

bash命令补全
> curl -L https://raw.githubusercontent.com/docker/compose/1.2.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
```

## YAML模板介绍
```
默认模板文件为docker-compose.yml,其中定义的每个服务都必须通过image指令或build指定（需要Dockerfile）来自动构建

如果使用build指定，在dockerfile中设置的选项，如CMD，EXPOSE，VOLUME，ENV等将会自动被获取，无需再次在docker-compose.yml中设置

image
如果指定镜像名或者id不存在，compose将会尝试拉取这个镜像
image: ubuntu:trusty

build
指定Dockerfile所在文件夹的路径。compose会利用它自动构建这个镜像，然后使用这个镜像。
build: /path/to/build/dir

command
覆盖容器启动后默认执行的命令
command: /bin/bash

links
链接到其他服务中的容器。使用服务名称（同时作为别名）或服务名称如
links:
    - db
    - db:database
    - redis

external_links
链接到docker-compose.yml外部的容器，甚至非compose管理的容器
external_links:
    - redis_1
    - project_db_1:mysql
    - project_db_1:postgresql

ports
暴露端口信息
使用HOST:CONTAINER格式或仅仅指定容器端口（宿主机随机选择端口）都可以
ports:
    - "3000"
    - "8000:8000"
    - "49100:22"
    - "127.0.0.1:8001:8001"
* 由于当使用容器端口小于60时YAML将会解析xx:yy这种数字格式为60进制，即得到错误结果，所以建议使用字符串

expose
暴露端口，但不映射到宿主机
expose:
    - "3000"
    - "8000"

volumes
卷挂载路径设置(HOST:CONTAINER OR HOST:CONTAINER:ro)
volumes:
    - /var/lib/mysql
    - cache/:/tmp/cache
    - ~/configs:/etc/configs/:ro
* 可以使用相对路径

volumes_from
从另一个服务或容器挂载它的所有卷
volumes_from:
    - service_name
    - container_name

environment
设置环境变量。你可以使用数组或字典两种格式。
environment:
    - RACK_ENV=development
OR
environment:
    RACK_ENV: development

env_file
从文件中获取环境变量，可以为单独的文件路径或列表。
env_file: .env
OR
env_file:
    - ./common.env
    - ./apps/web.env
    - /opt/secrets.env
环境变量每一行必须符合格式(KEY=VALUE)

dns
配置dns服务器，可以时一个值，也可以为列表
dns: 8.8.8.8
dns:
    - 8.8.8.8
    - 8.8.4.4

dns_search
可以为一个值，也可以为列表

ulimits
重写容器默认的ulimits,可以声明为单个整数或者soft/hard
nproc: 65535
nofile:
    soft: 20000
    hard: 40000
core: -1

其他（working_dir， hostname， user，mem_limit，privileged...）
working_dir: /code
hostname: foo
user: postgresql
mem_limit: 1000000000
privileged: true
```
