# DPDK一些杂项记录
```
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

## REF
    [grub2开机选项设置](https://wiki.centos.org/zh/HowTos/Grub2)
