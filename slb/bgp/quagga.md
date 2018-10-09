# quagga
```
此文档只是简单说明一些基本配置
```
## BGP Peer
### Define Peer```
```
bgp: neighbor peer remote-as asn
创建一个邻居，其中remote-as是asn，peer可以是ipv4，也可以是ipv6
示例：
    router bgp 1
     neighbor 10.0.0.1 remote-as 2
此命令必须是配置邻居时使用的第一个命令。
```
### BGP Peer commands
```
bgp:
  为peer设置描述
    neighbor peer description ...
    no neighbor peer description ...
  指定用于与该邻居的BGP会话的IPV4源地址
    neighbor peer update-source <ifname|address>
    no neighbor peer update-source
  如果路由通过eBGP学习的，该命令指定已宣布的路由的下一跳等同于bgp路由器的地址。如果all选项声明了，也会对iBGP学习的路由起作用
    neighbor peer next-hop-self [all]
    no neighbor peer next-hop-self [all]
```
### Peer filtering
```
bgp:
  指定对等方的分发列表,
    neighbor peer distribute-list name [in|out]
  在邻居上应用route-map
    neighbor peer route-map name [in|out]
````
## Filtering
```
过滤用于路由信息的输入和输出
```
### IP Access List
```
cmd: access-list <name> <permit|deny> ipv4-network
示例：
    允许2个网络进行转发，拒绝其他任何网络
    access-list private-only permit 192.168.0.0/24
    access-list private-only permit 192.168.1.0/24
    access-list private-only deny any
```
### IP Prefix List
```
ip prefix-list提供了最强大的基于前缀的过滤机制
cmd: ip prefix-list name (permit|deny) prefix [le len] [ge len]
cmd: ip prefix-list name seq number (permit|deny) prefix [le len] [ge len]
示例：
    ip prefix-list blackhole seq 5 permit 5.5.5.6/32
    ip prefix-list blackhole seq 10 permit 6.6.6.0/24

[seq]: seq可以自动或手动设置，但是需要小于4294967295
IP前缀匹配从较小的seq号到较大的seq号执行，一旦应用任何规则，匹配将停止
```
## Route Map
```
参见route-map部分的文档
https://www.nongnu.org/quagga/docs/docs-multi/Route-Map.html#Route-Map

```
## Ref
    [BGP 什么时候需要用 next-hop-self 与 ebgp-multihop 2]("https://blog.csdn.net/a9254778/article/details/41652915")
    [利用BGP community黑洞路由]("https://blog.gnuers.org/?p=1392")
