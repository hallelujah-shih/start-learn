# 汇聚一些LVS使用的问题

## 问题
  * LVS只转发了部分端口（检查下iptables）

## arp说明
```
Linux默认情况下，会对目标IP是本机地址的ARP请求做出响应，即使目标IP并没有配置到收到ARP请求的网络接口上。可以通过修改系统参数arp_announce和arp_ignore来调整ARP响应逻辑。

比如，禁止eth0响应目标地址配置在其他接口上的IP的ARP请求（LVS的DR模式需要配置）
echo 1 > /proc/sys/net/ipv4/conf/eth0/arp_ignore
echo 2 > /proc/sys/net/ipv4/conf/eth0/arp_announce
或通过/etc/sysctl.conf配置
net.ipv4.conf.eth0.arp_ignore = 1
net.ipv4.conf.eth0.arp_announce = 2
更新配置
sysctl -p
```
