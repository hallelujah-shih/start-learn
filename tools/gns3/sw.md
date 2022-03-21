# 基本概念

## vlan 功能
```
1. 隔离广播域
2. 在交换机这一层（数据链路层）可以规划网络
3. 只有在需要跨网传输的时候才需要3层设备
4. vlan可以从核心扩展到最边缘的交换机，可以理解为用二层设备实现了一部分三层的逻辑
```

## 汇聚口(trunk)
```
1. 可以通过所有vlan
2. 对于非默认vlan, 数据帧从这个口传输时家标签（tag）
3. 对于默认vlan，数据帧不会加标签
4. 加或不加标签只在数据帧从汇聚端口出入时发生
```

## 接入口(access)
```
1. 数据从这个口传输时也就是离开交换机时，没有标签（tag）
2. 所传输的必然为默认lan的数据帧
3. 即使有标签数据帧传输到这个口也会被丢弃
4. 所有接入端口在设备出厂时都是属于vlan1的传输口
5. 所有端口在设备出场时都是接入端口，而不是汇聚端口
```

## ref
    [vlan](https://www.youtube.com/watch?v=HnXWPO3Lhdc)