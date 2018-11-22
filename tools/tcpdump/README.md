# tcpdump
```
记录一些常用的TCPDUMP操作命令
```

## 抓取ssl/tls client hello报文
```
> tcpdump -i eth0 "tcp port 443 and (tcp[((tcp[12] & 0xf0) >> 2)] = 0x16) and (tcp[((tcp[12] & 0xf0) >> 2) + 5] == 0x01)" -p -s0 -w hello.cap -c 10000
```
