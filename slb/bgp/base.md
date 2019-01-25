# BGP
```
边界网关协议，是EGP（外部网关协议）的一种。
BGP的主要功能是在多个自治系统（AS）之间交换网络可达的信息，并强化路由策略（Policy），以及避免路由回路（routing loop）问题。
```
## BGP的路由属性
```
一些强制和非强制属性说明
```

### Well-known mandatory(著名强制类)
```
BGP的Update消息中，此类一定要出现在所有的Update消息中，用来叙述路由情形，传递给邻接BGP路由器。
```
#### AS-Path
```
AS-Path属性由一连串自治系统编号组成，用来提供到达目的网络的路由。
```
#### Next-Hop
```
BGP的Update消息中，Next-Hop属性用来指定下一跳（Hop）。
BGP区分出处理不同AS的路由（EBGP）和管理同一AS的路由（IBGP），所以Next-Hop属性上的使用有所不同
```

#### Origin
```
此属性表示路由的起源，即自治系统内产生路由更新的来源。也是Update消息中规定必须包含的消息。
属性有三种类型：
    * IGP：使用Network命令声明的网络，BGP会认为是同一个AS内部的路由
    * EGP：从外部网关（EGP）学习到的路由，
    * Incomplete：未完成的属性代表路由通过再分配方式注入BGP协议，此时Origin属性都会标记为Incomplete
```

### Well-known discretionary(著名非强制类)
```
BGP的Update消息中，著名非强制类消息不一定出现在其中
```
#### Local preference
```
Local Preference在同一个AS内才会被传送。
```
#### Atomic aggregate

### Optional transitive(选项转移类)

#### Aggretator

#### Community
```
这个属性是可以用来过滤路由的一种方法，用在一组路由中，可以拥有相同的路由选择策略，并非由单独的路由(IP Prefix)来决定，而不受限于硬件的界限，即一个自制系统内或一个网段内。
```

### Optional nontransitive(选项非转移类)
#### Multi-exit-discriminato(MED)

## BGP的路由选择
```
Cisco Router的BGP协议选择路由的顺序如下：
    1. 同一个自治系统内，在同步化是打开的情况下，若路由不同步，则不会送出路由信息。
    2. 若无法到达Next-Hop，则不使用这条路由，因此,IGP是取得Next-Hop的重要协议
    3. 选择较高权值（weight）的路由
    4. 若有相同的Weight，选择较高的Local Preference
    5. 若有相同的Local Preference，则选择产生路由的路由器
    6. 若相同Local Preference，都不是本身产生路由的路由器，则选择最短的AS-Path
    7. 若相同的AS-Path，则会选择最小的Origin Code，IGP<EGP<Incomplete，所以会偏好选择IGP
    8. 若Origin Code相同，则选择最小的MED值
    9. 若MED相同，则选择EBGP，再选择IBGP路由
    10. 若BGP Synchronization是OFF，而只有IGP协议，则会选择最短的BGP Next-Hop路由
    11. 选择最久的路由，再选择最小的邻接BGP Router ID
```
## BGP和EGP的异同
```
最大的不同是BGP在路由上加了权重，相同是都是采用Link State的路由选择协议。
````

# 内部网关协议（IGP）
```
IGP协议并没有一个广泛而通用的标准，这是由于各个自治系统内的网络使用的网络拓扑方式与网络技术不尽相同。如RIP、HELLO、IGRP、EIGRP、OSPF等
```
