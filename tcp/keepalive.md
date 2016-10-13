# TCP层的keepalive，非http协议的keepalive

## 系统中配置keepalive
### procfs接口
```
cat /proc/sys/net/ipv4/tcp_keepalive_time
cat /proc/sys/net/ipv4/tcp_keepalive_intvl
cat /proc/sys/net/ipv4/tcp_keepalive_probes

tcp_keepalive_time, tcp_keepalive_intvl参数都为秒
```

## 代码中使用keepalive
```
code: python

import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 7)
s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 5)
```

## 测试说明
```
socket层面通过发送ack数据包和应答的ack数据包来实现的

实际的测试效果来看（Fedora 23）,每次探测的间隔为tcp_keepalive_time
```

## reference
[TCP-Keepalive](http://www.tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/)
[python tcp keepidle](http://www.programcreek.com/python/example/28233/socket.TCP_KEEPIDLE)
