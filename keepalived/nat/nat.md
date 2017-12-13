# keepalived nat模式下的其他配置
## 防火墙配置
```
1. 在外网网口配置Nat模式（假设外网网口为eth0）
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# service iptables save
2. 配置内外网的转发规则
# iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
# iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
# iptables -A FORWARD -j REJECT --reject-with icmp-host-prohibited
# service iptables save
3. 增加被允许访问的服务或端口
# iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
# service iptables save
```

## 路由配置
```
" 配置后端服务器路由
# ip route add default via ${VIP} dev eth0
" 重启后永久加载
# echo "default via ${VIP} dev eth0" > /etc/sysconfig/network-scripts/route-eth0
```
