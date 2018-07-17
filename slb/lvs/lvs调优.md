# LVS调优
```
此处不兼顾老版本内核
```
## 调整ipvs connection hash表大小
```
IPVS connection hash table size，table size必须是2的幂，范围是[8,20]，默认为12，意为着table size默认为2^12 = 4096，不要设置太小，会影响性能（建议设置表的大小不要比每秒的连接数*平均持续的时间小太多）。
当ip_vs_conn_tab_bits=20时，对64位系统，IPVS大概占用16MB内存。

> ipvsadm -l
IP Virtual Server version 1.2.1 (size=4096)
这可以看到用的是默认值

# 查看是否被引用
> lsmod|grep ip_vs
# 移除ip_vs
> modprobe -r ip_vs
# 调整ip_vs模块的参数
# 1. 编辑/etc/modprobe.d/ip_vs.conf，增加options ip_vs conn_tab_bits=20
# 2. 重新挂载模块
> modprobe ip_vs
> ipvsadm -l
IP Virtual Server version 1.2.1 (size=1048576)
```

## Linux系统参数优化
### 关闭网卡LRO&GRO
```
LRO(large-receive-offload)
GRO(generic-receive-offload)
通过ethtool查看是否支持
> ethtool -k ${YOU_CONN}
暂时关闭
> ethtool -K ${YOU_CONN} gro off
# 可以设置在rc.local中，若有更优雅的办法，麻烦联系我（hallelujah.shih@gmail.com），不胜感激。
```
### 增大backlog
```
# 查看系统数值
> cat /proc/sys/net/core/netdev_max_backlog
# 我系统上为1000
# 修改/etc/sysctl.conf
net.core.netdev_max_backlog = 500000（每个网络接口接收数据包的速率比内核处理速度快时，允许送到队列的数据包的最大数目）
# 具体数值，咨询专家，设置合理的数值
```

### 网卡中断调优
```
主要思路是将中断分别绑定到CPU上，并关闭系统自动中断平衡服务
目的是为了优化大量网络数据包中断处理可能导致的网卡瓶颈。

引用https://my.oschina.net/kisops/blog/156561的自动化配置脚本
<bash>
#!/bin/bash  
# Enable RPS (Receive Packet Steering)  

rfc=4096  
cc=$(grep -c processor /proc/cpuinfo)  
rsfe=$(echo $cc*$rfc | bc)  
sysctl -w net.core.rps_sock_flow_entries=$rsfe  
for fileRps in $(ls /sys/class/net/eth*/queues/rx-*/rps_cpus)  
do
    echo fff > $fileRps  
done

for fileRfc in $(ls /sys/class/net/eth*/queues/rx-*/rps_flow_cnt)  
do
    echo $rfc > $fileRfc  
done

tail /sys/class/net/eth*/queues/rx-*/{rps_cpus,rps_flow_cnt}
</bash>
```

## 参考
	[LVS解决高并发](http://seitran.com/2015/04/13/01-gso-gro-lro/)
	[网卡TSO/GSO...](http://seitran.com/2015/04/13/01-gso-gro-lro/)
