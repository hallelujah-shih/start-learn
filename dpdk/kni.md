# KNI学习
```
DPDK的KNI允许用户空间程序访问Linux控制平面，好处如下：
    * 比现有的Linux TUN/TAP接口更快（消除了系统调用copy_to_user/copy_from_user）
    * 允许使用标准Linux网络工具(ethtool,ifconfig,tcpdump...)来管理DPDK端口
    * 提供了标准网络协议栈的接口
```
## DPDK KNI内核模块
```
此模块为两种类型的设备提供支持
1. 杂项设备(/dev/kni)：
2. 网络设备：
```

## KNI的创建和删除
```
KNI接口是由DPDK应用程序动态创建的。接口名称和FIFO详细信息由应用程序通过使用rte_kni_device_info结构的ioctl调用提供，其中包含：
    * 接口名称
    * 相关FIFO的相应memzones的物理地址
    * mbuf内存池的详细信息，包括物理和虚拟（用于计算mbuf指针的偏移）
    * PCI信息
    * CPU亲和
rte_kni_common.h中可以参见更多详情

KNI接口创建后可以被DPDK应用程序动态删除。所有未删除的KNI接口将会在其他设备的释放操作中删除。
```

## 示例KNI程序说明
```
程序主体结构：
    1. EAL初始化
    2. 传参分析
    3. 创建mbuf内存池(rte_pktmbuf_pool_create)
    4. kni子系统的初始化(rte_kni_init)
    5. 初始化每个端口（port统一说成端口，端口从属以太设备）
        a. rte_eth_dev_configure获取端口配置信息
        b. rte_eth_rx_queue_setup/rte_eth_tx_queue_setup初始化RX/TX队列
        c. rte_eth_dev_start启动端口
        d. rte_eth_promiscuous_enable，若有需要的，可以设置混杂模式
    6. 于各核上启动功能线程
    7. 程序清理，资源释放
```

## 程序运行
```
环境: 单网卡，开启KNI，且能内外相互通信为目的的测试
./kni -c 0x7 -- -p 0x1 --config "(0,1,2)"

可以用ifconfig查看网卡信息，这儿名字为vEth0
配置IP，GW并测试
> ip addr add 192.168.78.100/24 dev vEth0
> ip route add default via 192.168.78.2 dev vEth0

> ping domain.name
> telnet domain.name port

*** 注意，若测试不成功，可以将vEth0的MAC地址改为网卡本身的MAC地址
> ifconfig vEth0 hw ether 00:11:22:33:44:55
```

## 程序改造
```
1. 增加了UDP数据包的封禁
2. 所有192.168.78.10(VIP)的数据会转发到192.168.78.20的机器上（这儿我固定了MAC，正常应该是通过ARP获取），实现简单的LVS-DR测试
3. 所有syn报文，且TCP携带payload的数据包直接丢弃
```

## ref
    [kni mac](http://dpdk.org/dev/patchwork/patch/31796/)
    [修改的kni程序](./kni.c)
