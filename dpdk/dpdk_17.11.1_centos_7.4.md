#  DPDK开发环境搭建

## 系统以及DPDK版本信息
```
CentOS 7.4(Linux kernel 3.10.0，gcc 4.8)
DPDK 17.11.1(TLS)
```

## 依赖项安装
```
> yum -y install kernel-devel kernel-headers gcc gcc-c++ python-devel numactl-devel libpcap-devel git patch
```

## 源码打补丁
```
1. 下载DPDK源码17.11.1，并解压
> tar xvf dpdk.xxx
> cd dpdk-source-dir
2. 下载补丁
> curl -fLO https://raw.githubusercontent.com/iqiyi/dpvs/master/patch/dpdk-stable-17.05.2/0001-PATCH-kni-use-netlink-event-for-multicast-driver-par.patch
> curl -fLO https://raw.githubusercontent.com/iqiyi/dpvs/master/patch/dpdk-stable-17.05.2/0002-net-support-variable-IP-header-len-for-checksum-API.patch
3. 打补丁
> patch -p 1 < 0001-PATCH-kni-use-netlink-event-for-multicast-driver-par.patch
> patch -p 1 < 0002-net-support-variable-IP-header-len-for-checksum-API.patch

若igb_uio在VMWare下编译不过，且是RTE_INTR_MODE_LEGACY分支编译不过
修改if (pci_intx_mask_supported(udev->pdev))为if (pci_intx_mask_supported(udev->pdev) || true)
```

## 设置环境
```
设置DPDK环境变量
为了方便，于.bashrc中加入，自己替换dpdk-source-dir，RTE_TARGET根据自己机器配置
export RTE_SDK=${dpdk-source-dir}
export RTE_TARGET=x86_64-native-linuxapp-gcc
> source ~/.bashrc

设置hugepages，这里做1GB的设置示例
1. 修改grub(/etc/default/grub)
    在GRUB_CMDLINE_LINUX中加入default_hugepagesz=1G hugepagesz=1G hugepages=4
    如我机器的配置GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet default_hugepagesz=1G hugepagesz=1G hugepages=4"
2. 更新grub
    > grub2-mkconfig -o /boot/grub2/grub.cfg
3. 于/etc/fstab中添加自动挂载
    nodev /mnt/huge_1GB hugetlbfs pagesize=1GB 0 0
4. reboot
```

## 编译
```
> make config T=x86_64-native-linuxapp-gcc
> make -j
> make install T=x86_64-native-linuxapp-gcc
```

## 加载内核模块
```
> modprobe uio
> insmod build/kmod/igb_uio.ko
> insmod build/kmod/rte_kni.ko
若需要使用VFIO，需加载模块vfio-pci
```

## Hello World
```
我机器4核心
> cd $RTE_SDK/examples/helloworld
> make -j
> ./build/helloworld -c0x0f -n4
```

## loadbalancer
```
需要准备两张额外的网卡
我由于是vmware的虚拟机，所以我修改了RTE_INTR_MODE_LEGACY分支代码并重新编译，以及重新加载igb_uio模块
1. 绑定网卡(我这儿是ens34,35)
    > ./usertools/dpdk-devbind.py -b igb_uio ens34
    > ./usertools/dpdk-devbind.py -b igb_uio ens35
2. 运行程序
    > ./load_balancer -l 0-3 -n 4 -- --rx "(0,0,1),(1,0,1)" --tx "(0,1),(1,1)" --w "2,3" --lpm "1.0.0.0/24=>0; 1.0.1.0/24=>1;" --pos-lb 29
说明:
    由于我机器4核，所以-l选项填的是0-3
    --rx选项分别对应的(网卡,队列,逻辑核)我用的1核心处理收发报文
    --tx选项分别对应的(网卡,逻辑核)
    --w为业务处理逻辑核序号，我这儿用的是2,3核心
    --lpm配置，是子网表示=>转发口
    --pos-lb这儿是默认，没细看文档
```
