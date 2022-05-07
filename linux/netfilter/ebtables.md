# ebtables
```
Ethernet bridge frame table administration，以太网桥帧管理
```

## 表
```
Linux内核中有三个ebtables表，分别为filter、nat、broute，其中filter为默认表。

链（chains）的过滤顺序为：
prerouting: 数据进来之前的规则，不查询路由表
input: 负责过滤目的地址为本机的数据包
forward: 负责转发流过主机但不进入本机的数据包
postrouting: 查询路由表后要转发的规则
output: 负责处理本机发送的数据包

目标（targets）说明：
ACCEPT：表示让一帧通过 （broute中，表示该帧必须桥接）
DROP：表示丢弃该帧（broute中，表示该帧必须被路由）
CONTINUE：表示将检查下一条规则（rule）
RETURN：表示停止遍历这条链，并在上一条调用链的下一条规则中恢复
```

### 表-filter
```
默认过滤表，内置三条链：
INPUT: 在MAC目标地址层面上，以网桥本身为目的地的帧
OUTPUT: 本地构建的帧或者(b)routed帧
FORWARD: 为网桥转发的帧
```

### 表-nat
```
用于nat转换的表，更改源和目​​标mac地址，包含三个内置链：
PREROUTING: 帧进入就进行更改（snat）
OUTPUT:
POSTROUTING: 用于dnat
```

### 表-broute
```
用来做桥接路由器的，有一个内置链:
BROUTING: 
    DROP和ACCEPT在broute表中有特殊含义，其中DROP实际上意味着该帧必须被路由，而ACCEPT意味着该帧必须被桥接。
```

## ref
    [ebtables](https://blog.fearcat.in/a?ID=01550-3fd2e3b8-7682-40cf-bbd7-a4a86574afdb)