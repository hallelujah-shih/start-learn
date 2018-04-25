# DPDK一些杂项记录
```
```

## 编程基础
```
CPU相关的基本概念
处理器核数（CPU cores）：每个物理CPU核心个数
逻辑处理器核心数（siblings）：单个物理处理器超线程的个数
系统物理处理器封装ID（physical id）：也称为socket插槽，物理机处理器封装个数，物理CPU个数
系统逻辑处理器ID（processor）：逻辑CPU数，是物理处理器的超线程技术
在DPDK中会用到lcore,socket以及NUMA

一些基本概念的说明和解释
核心组件架构参见(https://dpdk.org/doc/guides/prog_guide/overview.html)

dpdk程序的基本结构
1. eal的初始化
2. 进行参数解析(dpdk的和应用层)
3. 分配报文的mempool
4. 初始化以及启动接口
5. 启动各个核上的线程
6. 等待线程退出，进行最后处理
```

### EAL
```
EAL: Environment Abstraction Layer，环境抽象层，是DPDK背后的主要概念
EAL是一组编程工具，使得DPDK能在特定的硬件环境和操作系统下工作，在DPDK库中，库和驱动是作为EAL的一部分放在rte_eal目录中，还包含了各种处理器架构的一组头文件。
最常见的头文件包括:
    rte_lcore.h 管理处理器和套接字
    rte_memory.h 管理内存
    rte_pci.h 提供了访问PCI地址空间的接口
    rte_debug.h ...
    rte_interrupts.h 处理中断
```

### 队列管理
```
此功能由rte_ring提供
网卡接受的数据包会被发送到环形缓冲区，它充当了接收队列。在DPDK中收到的数据包也会发送到rte_ring库上实现的队列中。
rte_ring是基于FreeBSD的ring buffer。
该队列是建立在FIFO原理上的无锁环形缓冲区，主要包含4类:
    prod_tail
    prod_head
    cons_tail
    cons_head
其中prod是producer简写，cons是consumer的简写
环形缓冲区写入的地方是tail
环形缓冲区读取的地方是head
```

### 内存管理
```
此功能在rte_mempool中提供
DPDK需要hugepages，这些页面按分段组合，然后分为多个区域。由应用程序或库（如队列，数据包缓冲区）创建的对象存于这些区域中。
这些对象包括由rte_mempool库创建的内存池
为了防止性能瓶颈，每个核心在内存池中都有一个额外的本地缓存.
```

### 缓冲区管理
```
此功能由rte_mbuf提供
在Linux网络堆栈中，所有网络数据包均由sk_buff数据结构表示。在DPDK中，这是使用rte_mbuf结构完成的，该结构在rte_mbuf.h头文件中有描述。
DPDK的缓冲区管理方式，不是使用一个大的sk_buff结构，而是许多较小的rte_mbuf缓冲区。缓冲区在DPDK应用程序启动之前创建并保存在内存池中,内存由rte_mempool分配。
```

### 时间管理
```
此功能由rte_timer提供
该库为DPDK执行单元提供定时服务，提供异步执行功能的能力。
```

### 数据包转发算法支持
```
DPDK包含Hash（rte_hash）和最长前缀匹配（LPM, rte_lpm）库，用于支持数据包的转发算法。
```

### Makefile说明
```
1. 应用程序Makefile
    开头: include $(RTE_SDK)/mk/rte.vars.mk
    结尾: include $(RTE_SDK)/mk/rte.extapp.mk

    必须定义的变量:
        APP: 应用程序的名字
        SRCS-y: 源文件列表(*.c,*.S)
2. 库Makefile
    与应用程序Makefile相比，唯一差别是将APP变量变成LIB，当然名字值也要调整，如libfoo.a

3. 其他
    除了固定结构外，可以对一些变量做调整，详情见DPDK文档，如下:
    VPATH
    CFLAGS_my_file.o
    CFLAGS
    CPPFLAGS
    LDFLAGS
    LDLIBS
```

## 杂项

### HugePages说明
```
关于HugePages的设置，可以先查看CPU标志支持多大的
若 pse 标志存在说明2M的HugePages支持
若 pdpe1gb 标志存在，说明支持1G的HugePages
如:
> grep pse /proc/cpuinfo

查看系统HugePages的信息
> grep Huge /proc/meminfo
AnonHugePages:     14336 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
可以看到我机器上没有配置Hugepagesizes，以及默认的Hugepagesizes的大小为2M

对于单节点系统,可以使用下面命令设置hugepages
> echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
对于NUMA机器就需要对每个点单独设置hugepages，如
> echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
> echo 1024 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages

hugepage重启自动应用,需在/etc/sysctl.conf加入
vm.nr_hugepages=1024

DPDK使用hugepages
> mkdir -p /mnt/huge
> mount -t hugetlbfs nodev /mnt/huge

重启自动应用，需在/etc/fstab中加入
nodev /mnt/huge hugetlbfs defaults 0 0
如果是1GB的页,pagesize需要在挂载选项中显式说明
nodev /mnt/huge_1GB hugetlbfs pagesize=1GB 0 0

跑helloworld程序可能会出现
No free hugepages reported in hugepages-1048576kB
说在hugepages-1048576kB中没有空余的hugepages，可以在/sys/kernel/mm/hugepages目录中看到可能存在
hugepages-1048576kB  hugepages-2048kB，即同时支持1G和2M的，而上面配置的2M的（http://dpdk.org/ml/archives/users/2017-December/002747.html）

配置1G默认页,以CentOS 7为例
首先，1G页必须在开机选项中配置
在/etc/default/grub文件的GRUB_CMDLINE_LINUX中加入'default_hugepagesz=1G hugepagesz=1G hugepages=4'，这儿表示预留4G空间，可以大于实际物理内存
生成grub2配置
> grub2-mkconfig -o /boot/grub2/grub.cfg
UEFI是
> grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg

Ubuntu 
在/etc/default/grub中添加
GRUB_CMDLINE_LINUX_DEFAULT="default_hugepagesz=1G hugepagesz=1G hugepages=4"
更新grub
> update-grub
```

### NUMA系统
```
源于AMD Opteron微架构,处理器和本地内存之间有更小的延迟和更大的带宽；每个处理器还可以有自己的总线。处理器访问本地的总线和内存时延迟低，而访问远程资源时则要高。
```

### 驱动加载
```
不同的PMD可能需要不同的内核驱动，取决于正在使用的PMD，相应的内核驱动程序应该加载并绑定到网络端口上

UIO：
许多情况下Linux内核中包含的标准uio_pci_generic模块可以提供uio功能
> modprobe uio_pci_generic 注意，此模块不支持虚拟功能的创建
作为uio_pci_generic的替代方案，DPDK提供了igb_uio模块
> modprobe uio
> insmod $RTE_SDK/build/kmod/igb_uio.ko
DPDK 1.7提供了VFIO的支持，支持使用VFIO的平台，使用UIO是可选的
> modprobe vfio-pci
内核3.6.0后通常包含VFIO模块，且通常为默认存在，如果要使用VFIO，必须加在vfio-pci模块，另外要使用VFIO，内核和BIOS必须支持并配置使用IO虚拟化
vfio-pci不支持创建虚拟功能
```

## 程序小片段
```

```

## REF
    [grub2开机选项设置](https://wiki.centos.org/zh/HowTos/Grub2)
