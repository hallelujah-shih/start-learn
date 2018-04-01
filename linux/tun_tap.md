# TUN TAP接口的理解
```
Linux和大多数操作系统都有创建TUN/TAP接口的能力。
通常，系统中的网络设备（如eth0）都是存在与之关联的物理设备，用于将数据包放在线路上。相对的,TUN或TAP设备是完全虚拟的，是由内核管理的。用户空间的程序可以与TUN和TAP设备进行交互，就像真实的一样，操作系统会将数据包推入或注入到常规网络栈中，从而看起来就像在使用真实的设备。
```

## TUN接口
```
TUN设备工作在网络栈的IP层或三层，通常是点对点连接。TUN设备典型用途是建立VPN连接，因为它使VPN软件有机会在数据加载前加密数据。由于TUN设备在第三层工作，因此只接受IP包，在某些情况下只能使用IPv4。如果你需要在TUN设备上运行任何其他协议，那么您运气不好。另外，因为TUN设备在第三层工作，所以它们不能用于网桥，并且通常不支持广播。
```

## TAP接口
```
相比之下，TAP设备工作在以太层或第二层，因此表现得非常像真正的网络适配器。由于在二层运行，所以可以传输任何三层协议，并且不限于点对点的连接。TAP设备可以成为网桥的一部分，并且通常用于虚拟化系统，为多个访客机器提供虚拟的网络适配器。由于TAP将转发广播报文，这通常使得他们成为VPN连接的不好选择。
```

## 管理虚拟接口
```
添加
> ip tuntap add name tap0 mode tap
> ip link show
删除
> ip tuntap del dev tap0 mode tap
```

### 创建veth pairs
```
可以创建一对连接接口，通常称为veth pair，用作虚拟接线。从本质上将你创建一个跳线的虚拟等价物。
以下将创建一对ep1和ep2的链接接口
> ip link add ep1 type veth peer name ep2
并为设备添加IP地址
> ip addr add 10.0.0.10 dev ep1
> ip addr add 10.0.0.11 dev ep2
可以使用ping测试连通性
> ping -I 10.0.0.11 -c4 10.0.0.10
> ping -I 10.0.0.10 -c4 10.0.0.11
```

## ref
	[理解TUN TAP接口](http://www.naturalborncoder.com/virtualization/2014/10/17/understanding-tun-tap-interfaces/)
	[Monitoring and Tuning the Linux Networking Stack: Sending Data](https://blog.packagecloud.io/eng/2017/02/06/monitoring-tuning-linux-networking-stack-sending-data/)
