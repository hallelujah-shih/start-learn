# ss安装和使用
```
目的，懂的
```

## 地址
[ss](https://github.com/shadowsocks/shadowsocks)

## 搬瓦工
```
vim /etc/security/limits.conf
增加进程能打开的最大句柄数
* soft nofile 51200
* hard nofile 51200

vim /etc/sysctl.conf
增加如下配置
fs.file-max = 51200

net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.netdev_max_backlog = 250000
net.core.somaxconn = 4096

net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 5000
#net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_mem = 25600 51200 102400
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_congestion_control = hybla

执行 sysctl -p
搬瓦工上若出现permission denied on key 'net.nf_conntrack_max'
据说是openvz的模板问题
修复modprobe的：

rm -f /sbin/modprobe 
ln -s /bin/true /sbin/modprobe
修复sysctl的：

rm -f /sbin/sysctl 
ln -s /bin/true /sbin/sysctl
```
