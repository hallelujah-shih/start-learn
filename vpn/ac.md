# 搭建anyconnect服务器
    centos7.1为例

## 准备工作
```
拉代码（http://www.infradead.org/ocserv/download.html）
> git clone https://gitlab.com/ocserv/ocserv.git

安装依赖
> yum -y install epel-release
> yum -y update 
> yum -y upgrade
> yum -y install gnutls-devel libev-devel protobuf-c-compiler

安装可选依赖（一些特定功能使用）
> yum -y install tcp_wrappers-devel pam-devel lz4-devel libseccomp-devel readline-devel libnl3-devel krb5-devel liboath-devel radcli-devel

git的代码编译安装需要安装gcc, autoconf, automake, autogen, git2cl, and xz
> yum -y install gcc automake autoconf autogen git2cl xz
```

## 代码编译
```
> cd ocserv
> chmod +x autogen.sh
> ./autogen.sh
> ./configure && make
```

## 配置
