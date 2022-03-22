# 基本概念

## vlan 功能
```
vlan提供了两个核心功能
1. 将物理交换机分解为虚拟的 "迷你交换机"
2. 将虚拟 "迷你交换机 "扩展到多个物理交换机上

VLANs允许你的逻辑拓扑结构不受物理拓扑结构的限制
```

## 汇聚口(Trunk Ports / Tagged Ports)
```
承载多个vlan流量的端口
```

## 接入口(Access Ports / Untagged Ports)
```
仅承载一个vlan流量的端口
    * 所有穿过Trunk端口的帧都必须被 "标记（tagged）"，以便接收的交换机知道将该流量与哪个VLAN相关。
```

## 802.1q
```
如何在二层（layer 2 frames）打tag的标准
```

## Native VLAN
```
穿过Trunk/Tagged链路的一个VLAN，没有VLAN标签。
```

## Configuring VLANs on Cisco Switches
```
基本配置命令
```

### 创建vlan
```
1. 创建vlan
SwitchX(config)# vlan 10
2. 为vlan命名（便于识别）
SwitchX(config-vlan)# name IT
```

### 将交换口分配给vlan
```
SwitchX(config)# interface Ethernet 0/0
1. 设定交换口为access ports
SwitchX(config-if)# switchport mode access
2. 将port指定为vlan 10
SwitchX(config-if)# switchport access vlan 10
```

### 汇聚口（Trunk Ports）
```
SwitchY(config)# interface Ethernet1/1
1. 设置为汇聚口
SwitchY(config-if)# switchport mode trunk

* 封包方式可以显式指定
SwitchX(config)# interface Ethernet1/1
1. 强制使用802.1q标准封包
SwitchX(config-if)# switchport trunk encapsulation dot1q
2. 设置为汇聚口
SwitchX(config-if)# switchport mode trunk
```

### Native VLAN
```
本地VLAN是主干端口上允许保持无标记的一个VLAN。默认情况下，它被设置为VLAN 1，但这可以由管理员改变。

SwitchX(config)# interface Ethernet 1/1
1. 设置Native vlan
SwitchX(config-if)# switchport trunk native vlan 2
设置此命令后，任何时候SwitchX在VLAN 2上向trunk port Eth1/1发送流量时，都将不添加VLAN标签。此外，任何时候SwitchX在trunk port Eth1/1上收到未加标签的流量，SwitchX将把该流量分配给VLAN 2。

** 若两交换机的trunk port相连，两个trunk port必须要有相同的vlan。否则，你很容易有这样的风险：一个VLAN中的主机能够与另一个VLAN中的主机通信。
```

### 允许的vlan列表
```
方法1
SwitchX(config)# interface Ethernet 2/1
SwitchX(config-if)# switchport trunk allowed vlan 10,20

方法2
SwitchX(config)# interface Ethernet 2/2
SwitchX(config-if)# switchport trunk allowed vlan 20
SwitchX(config-if)# switchport trunk allowed vlan add 30
如果少了一个add，将会被覆盖

移除：
SwitchX(config)# interface Ethernet1/1
SwitchX(config-if)# switchport trunk allowed vlan remove 20
移除所有
SwitchX(config-if)# no switchport trunk allowed vlan
```

## 显示

### vlan概要
```
SwitchX# show vlan brief
显示交换机上的access ports的概要信息：
存在于交换机VLAN数据库中的VLAN。
每个VLAN中配置的access ports
```

### show interfaces trunk
```
SwitchX# show interfaces trunk
显示交换机上的trunk ports的命令
其中生成树协议（STP: Spanning Tree Protocol）的存在是为了确保L2域不包含任何环路。
```

### show interfaces switchport
```
SwitchX# show interfaces Ethernet 0/1 switchport
显示交换机接口的详细信息，其中输出描述说明
switchport: 如果端口作用L2，则启用；如果端口作用L3，则禁用
```
### show interfaces status
```
SwitchX#   show interfaces status
```

### show spanning-tree
```
SwitchX# show spanning-tree vlan 10
提供有关access ports和trunk ports的信息
```

## 私有Vlan(Private VLAN, PVLAN)
```
也称为端口隔离，是一种针对二层网络的网络分段技术，可以实现同一IP段下的端口隔离或流量分段。通过在共享网络环境中应用私有VLAN，极大的节省了IP地址，提高二层交换机端口的安全性。
```
### 术语介绍

#### PVLAN端口类型(通常3种)
##### Promiscuous Port(混杂端口)
```
此端口类型能够从 VLAN 中的任何其他端口发送和接收帧。它通常与第 3 层交换机、路由器或其他网关设备连接。
```
##### Isolated Port(隔离端口)
```
存在于子VLAN中，隔离端口与主机相连，只能与混杂端口通信。
```
##### Community Port(社区端口)
```
社区端口也驻留在子 VLAN 中，并与主机连接。但是，它只能与混杂端口和同一子 VLAN 中的其他社区端口通信。
```
#### PVLAN的VLAN类型
```
在私有VLAN中，可以通过三种类型访问VLAN
```
##### Primary VLAN(主VLAN)
```
这种类型的 VLAN 是指原始 VLAN，它可以将帧从混杂端口下行到所有子VLAN(sub-VLANs, secondary VLA Ns)到所有与主机连接的端口。
```
##### Isolated VLAN(隔离VLAN)
```
隔离VLAN作为secondary VLAN，只能支持隔离VLAN内的交换机端口（隔离端口:Isolated Port）向主VLAN中的混杂端口转发数据。即使在同一个隔离 VLAN 中，隔离端口也不能相互通信。
```
##### Community VLAN(社区VLAN)
```
社区 VLAN 也是secondary VLAN 的一种。同一社区 VLAN 内的交换机端口（社区端口）可以相互通信，也可以与主 VLAN 的端口通信。但这种类型的 VLAN 也无法与其他辅助 VLAN 通信，包括其他社区 VLAN。
```
## ref
    [vlan](https://www.practicalnetworking.net/stand-alone/vlans-the-simplest-explanation/)
    [switch cfg](https://www.practicalnetworking.net/stand-alone/configuring-vlans/)
    [pvlan](https://community.fs.com/blog/what-is-private-vlan-and-how-it-works.html)
    [VXLAN](https://support.huawei.com/enterprise/zh/doc/EDOC1100087027)
