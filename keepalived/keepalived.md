# 安装和配置keepalived
```
1. 安装软件
# yum -y install keepalived
2. 编辑/etc/keepalived/keepalived.conf
3. 允许IP转发
# echo "net.ipv4.ip_forward = 1">>/etc/sysctl.conf
# sysctl -p
4. 增加防火墙规则允许VRRP协议通信
# iptables -I INPUT -i ${YOU_CONN} -d 224.0.0.0/8 -p vrrp -j ACCEPT
# iptables -I OUTPUT -o ${YOU_CONN} -d 224.0.0.0/8 -p vrrp -j ACCEPT
# service iptables save
5. 允许服务自启动
# chkconfig keepalived on
# service keepalived start
```

## NAT配置示例
```

```

## DR配置示例
```
```

## TUN配置示例
```
```

