# 系统DNS相关杂项

## 在NetworkManager+systemd-resolved管理的DNS解析中

### 设置全局解析为指定地址
```
设置全局解析地址为： 127.0.0.1:5553
编辑：/etc/systemd/resolved.conf
DNS=127.0.0.1:5553

sudo systemctl restart systemd-resolved.service 
```

### 忽略某些线路上DHCP中得到的DNS Server
```
编辑：/etc/NetworkManager/system-connections 目录下的指定 id 的连接文件
[ipv4]
ignore-auto-dns=true

或者 nmcli c e id
> set ipv4.ignore-auto-dns=yes
```

## 查看
```
resolvectl dns 或 resolvectl status
```