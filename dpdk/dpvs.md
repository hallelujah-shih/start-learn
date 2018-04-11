# DPVS基本使用记录
```
本文档记录一些DPVS相关的基本东西
本文基于CentOS 7.4(3.10.0-693.21.1.el7.x86_64)
```

## 依赖安装
```
除了DPDK正常的安装以外，此处单独说DPVS的依赖(与DPVS结合的DPDK版本我选择的是17.05.2)
> yum -y install openssl-devel numactl-devel popt-devel
模块加载
> modprobe uio 
> insmod $RTE_SDK/build/kmod/igb_uio.ko
> insmod $RTE_SDK/build/kmod/rte_kni.ko
```

## 编译
```
> make -j
> make install
```

## 使用（DR模式，单网卡）
```
dpdk绑定一张网卡（ens34）
> dpdk-devbind.py -b igb_uio ens34

配置文件处理
> cp conf/dpvs.conf.single-nic.sample /etc/dpvs.conf
并根据自己机器的CPU以及tx/rx-queue的大小调整配置文件

启动dpvs
> bin/dpvs

可以通过命令查看启动是否OK
> bin/dpip link show

添加LAN IP，且必须在VIP前添加(网段为192.168.78.0/24, gw为192.168.78.2/24)
> bin/dpip addr add 192.168.78.100/24 dev dpdk0
添加VIP
> bin/dpip addr add 192.168.78.10/32 dev dpdk0

添加LVS服务
> bin/ipvsadm -A -t 192.168.78.10:80 -s wrr -p 300
> bin/ipvsadm -a -t 192.168.78.10:80 -r 192.168.78.20:80 -g

测试VIP访问
> curl 192.168.78.10 -v >/dev/null
```

## ref
    [ipvs doc](https://github.com/iqiyi/dpvs/blob/master/doc/tutorial.md#dr)
