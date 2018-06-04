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

配置kni端口
> ip addr add 192.168.78.100/24 dev dpdk0.kni
> ip route add default via 192.168.78.2 dev dpdk0.kni
检查配置
> ifconfig
> ping domain.name
若虚拟机环境，ping不通，需要将ether的地址改为网卡开始的mac地址
> ifconfig dpdk0.kni hw ether 00:11:22:33:44:55
# > ip link set dev dpdk0.kni address 00:11:22:33:44:55

端口上配置LAN IP
> bin/dpip addr add 192.168.78.100/24 dev dpdk0
端口上配置VIP
> bin/dpip addr add 192.168.78.10/32 dev dpdk0

添加LVS服务
> bin/ipvsadm -A -t 192.168.78.10:80 -s wrr -p 300
> bin/ipvsadm -a -t 192.168.78.10:80 -r 192.168.78.20 -g

测试VIP访问
> curl 192.168.78.10 -v >/dev/null

测试LB机器到RS机器是否OK
> nc 192.168.78.20 80
```

## ref
    [ipvs doc](https://github.com/iqiyi/dpvs/blob/master/doc/tutorial.md#dr)
