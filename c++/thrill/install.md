# 使用thrill准备
```
以ubuntu 14.04 LTS为示例
```

## 环境准备
```
> sudo apt-get install git cmake autoconf libtbb-dev libbz2-dev zlib1g-dev libxml2-dev libcurl4-openssl-dev libboost-all-dev
> sudo add-apt-repository ppa:ubuntu-toolchain-r/test
> sudo apt-get update
> sudo apt-get install gcc-6 g++-6
> sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6
```

## 编译
```
> git clone https://github.com/thrill/thrill.git
> cd thrill && ./compile.sh
```
