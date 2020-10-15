FROM ubuntu:trusty

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt-get update

RUN apt-get install build-essential vim gdb -y

CMD /bin/bash
