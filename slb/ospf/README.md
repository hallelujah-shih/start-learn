# ospf简单说明
```
开放最短路径优先协议，是AS内的一种路由选择协议
```

## 负载均衡配置
```
这里以思科的三层交换机为例（思科所有三层交换机均支持ospf）
```

### 交换机
```
这里假设划分的vlan为225
# ip routing
# router ospf 1
# router-id 192.168.1.1
# interface Vlan225
# ip ospf network broadcast
# ip ospf 1 area 0
```

### 服务器
```
这里以CentOS 7.5为测试服务器，用quagga为例
以下操作为实验环境，直接关闭了selinux,firewalld

# 安装quagga
> yum install quagga

# 启动zebra
> cp /usr/share/doc/quagga-xxx/zebra.conf.sample /etc/quagga/zebra.conf
> systemctl enable zebra
> systemctl start zebra

# 配置并启动ospfd（如下操作在所有ospfd服务器上一样，除了router-id和ip/24的配置）
> cp /usr/share/doc/quagga-xxx/ospfd.conf.sample /etc/quagga/ospfd.conf
编辑ospf.conf，配置router ospf相关信息，如下：
! 这里本机IP为192.168.1.2/24,其中VIP从192.168.1.100-192.168.1.126
    router ospf
        ospf router-id 192.168.1.2
        network 192.168.1.2/24 area 0
        network 192.168.1.100/32 area 0
        ....
> systemctl enable ospfd
> systemctl start ospfd

# 在lo口上配置VIP
> for i in {100..126}; do ip addr add 192.168.1.$i/32 dev lo; done
```

## 状态检查
```
检验的标准：期望流量能分配到所有配置了OSPFD服务的服务器上
```

### 主机上检查
```
>vtysh
# 查看链路状态数据库
> show ip ospf database

# 查看邻居表
> show ip ospf neighbor
```

### 交换机上状态查看
```
标准:
当确定了交换机使用per-destination load sharing algorithm就OK
当确定了交换机的ip router，vip同时指向所有配置了的ospfd服务器地址即可

> enable
# 查看路由信息
> show ip router
# 其中就能看到先前配置的/32地址有多个目标，或者可以使用 show ip cef，也可以清晰的看到每个ip的next-hop信息(也是多个ospfd服务器地址)

# 确认快速转发所用算法
> show cef state
CEF Status:
 RP instance
 common CEF enabled
IPv4 CEF Status:
 CEF enabled/running
 dCEF enabled/running
 CEF switching enabled/running
 universal per-destination load sharing algorithm, id 166D0548
IPv6 CEF Status:
 CEF disabled/not running
 dCEF disabled/not running
 universal per-destination load sharing algorithm, id 166D0548
能看出使用的是universal per-destination load sharing algorithm，是通过src,dst,id共同决定路由转发的，所以可以放心使用

# 可以根据需要调整快速转发算法
> configure terminal
# 可以指定ID，不指定为随机ID
> ip cef load-sharing algorithm universal
```


