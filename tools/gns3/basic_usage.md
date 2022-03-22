# basic usage

## 镜像预下载
```
https://mega.nz/folder/nJR3BTjJ#N5wZsncqDkdKyFQLELU1wQ
此处我选择了c3725 & c7200下载
```

## 启动gns3
```
edit -> preferences
Dynamips: IOS routers
选择new并导入下载的镜像
```

## 说明
```
- NM-1E        (Ethernet, 1 port)
- NM-4E        (Ethernet, 4 ports)
- NM-1FE-TX    (FastEthernet, 1 port)
- NM-16ESW     (Ethernet switch module, 16 ports)
- NM-NAM
- NM-IDS
- WIC-1T (1 Serial port)
- WIC-2T (2 Serial ports)
```
## 简单配置router
```
R1# configure terminal
R1(config)# interface f0/0
R1(config-if)# ip address 10.0.0.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# end
```

## 示例
```
拓扑(ospf)
pc1 ---10.0.1.0/24---  r1  ---172.16.0.0/16--- r2 ---192.168.0.0/24--- pc2
r1:
R1# configure terminal
R1(config)# interface f0/0
R1(config-if)# ip address 172.16.0.1 255.255.0.0
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface f0/1
R1(config-if)# ip address 10.0.1.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# router ospf 1
R1(config-router)# network 10.0.1.0 0.0.0.255 area 0
R1(config-router)# network 172.16.0.0 0.0.255.255 area 0
R1(config-router)# end
R1# write

r2:
R2# configure terminal
R2(config)# interface f0/0
R2(config-if)# ip address 172.16.0.2 255.255.0.0
R2(config-if)# no shutdown
R2(config-if)# exit
R2(config)# interface f0/1
R2(config-if)# ip address 192.168.0.1 255.255.255.0
R2(config-if)# no shutdown
R2(config-if)# exit
R2(config)# router ospf 1
R2(config-router)# network 192.168.0.0 0.0.0.255 area 0
R2(config-router)# network 172.16.0.0 0.0.255.255 area 0
R2(config-router)# end
R2# write

R2# show ip ospf neighbor
R2# show ip route

pc1:
PC1> ip 10.0.1.2/24 10.0.1.1
PC1> ping 192.168.0.2

pc2:
PC2> ip 192.168.0.2/24 192.168.0.1
PC2> ping 10.0.1.2
```

## ref
    [Difference between Ethernet vs Fast Ethernet vs Gigabit Ethernet](https://www.rfwireless-world.com/Terminology/Ethernet-vs-Fast-Ethernet-vs-Gigabit-Ethernet.html)
    [10 commands you should master when working with the Cisco IOS](https://www.techrepublic.com/blog/data-center/10-commands-you-should-master-when-working-with-the-cisco-ios-104071/)
    [OSPF configuration](https://study-ccna.com/ospf-configuration/)
