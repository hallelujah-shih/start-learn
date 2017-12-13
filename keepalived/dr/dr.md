# dr模式其他配置
```
dr模式要求在主keepalived服务器和后端服务器上都配置虚拟IP地址。keepalived服务维护虚拟IP于主keepalived服务器上。
只有主keepalived服务器响应虚拟IP地址的ARP请求。所以需要为每个后端服务器的网络接口设置arp_ignore和arp_announce参数，避免响应虚拟IP地质的ARP请求。
```

## 配置防火墙
```
增加允许访问的服务或端口
# iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
# service iptables save
```

## 后端服务器的必要配置
```
1. 配置ARP相关参数
" dr模式虚拟IP地址可以配置在后端服务器lo口上，当然主网口、另创建接口都可以，这里用主网卡eth0
# echo "net.ipv4.conf.eth0.arp_ignore = 1" >> /etc/sysctl.conf
# echo "net.ipv4.conf.eth0.arp_announce = 2" >> /etc/sysctl.conf
# sysctl -p
2. 固化虚拟地址到eth0口
# echo "ip addr add ${VIP} dev eth0" >> /etc/rc.local
3 .reboot
```
