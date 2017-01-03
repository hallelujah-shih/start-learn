FROM ubuntu:trusty

MAINTAINER Hallelujah<sh19871122@gmail.com>

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt-get update && apt-get install -y \
        build-essential \
        wget \
        curl \
        make \
        unzip \
        gdb tmux python-pip \
        python-dev  \
        libzookeeper-mt-dev \
        git

RUN mkdir -p /root/.pip/ && echo "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\ntrusted = mirrors.aliyun.com" > /root/.pip/pip.conf

RUN pip install zkpython

RUN wget https://github.com/phunt/zk-smoketest/archive/master.zip -O zk-smoketest.zip; \
        unzip zk-smoketest.zip; \
        rm zk-smoketest.zip

