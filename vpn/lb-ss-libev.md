# 架设SS服务的LoadBalancer
```
由于系统升级后qt-ss启动找不到动态库，不想折腾，直接上 haproxy + shadowsocks-libev架构
本文基于fedora 29上的操作
```
## 安装&配置shadowsocks-libev
```
> sudo dnf -y install shadowsocks-libev

config1.json:
    {
        "server": "remote_ip",
        "server_port": 1024,
        "local_address": "127.0.0.1",
        "local_port": 1083,
        "password": "passwd",
        "timeout": 60,
        "method": "rc4-md5"
    }

config2.json:
    ...

通过服务启动ss:
> ss-local -c configx.json >/dev/null 2>&1
```
## 安装&配置haproxy
```
> sudo dnf -y install haproxy
> sudo cp my_local_proxy.cfg /etc/haproxy/haproxy.cfg
> sudo /sbin/restorecon -v /etc/haproxy/haproxy.cfg
> sudo setsebool -P haproxy_connect_any=on
> sudo systemctl enable haproxy
> sudo systemctl start haproxy
```
## REF
    [我的简单配置文件](./haproxy.cfg)
