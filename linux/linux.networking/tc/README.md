# HTB排队规则(HTB Queuing discipline)
```
Linux流控功能集的一部分，可以控制网络流量的排队，以及控制网络流量的排队规则。

TC机制是在IP数据包排队传输后进行的，主要涉及4部分：queuing discipline、class、filter、policing.
```

## Queuing Discipline
```
主要分为两大类
classful qdisc(有类别的qdisc):
    是灵活的，允许将子classful qdisc附着在上，叶子类上的qdisc会有一个classless qdisc。
    HTB
    CBQ

classless qdisc(无类别的qdisc):
    是基本或者初级的qdisc，不能有子qdisc附着在上面，也不能共享带宽。
    pfifo,bfifo,pfifo_fast(default),tbf,sfq等
```

## class
```
服务类别定义了策略规则（policing rules），如最大带宽、最大突发带宽等。
其中Queuing Discipline和一个class关联在一起的，一个类所定义的规则必须与一个预定义的队列相关联。
大多数情况下，每个类拥有一个queue discipline，但也可能几个类共用一个queue discipline。
```

## Filter
```
filters定义了queuing discipline使用的规则，queuing discipline通过使用filter来决定需要将数据包分配到哪个类别（class）。每个filter都有一个指定的优先级，并根据优先级按升序排列，每个queuing discipline可以有一个或者多个filter关联。
```

## Policing
```
policing确保流量不超过定义的带宽，而policing的控制决策是基于filter和class的rules的。
```

## 命令
```
tc qdisc: 创建 queuing discipline
tc class: 创建 class
tc filter: 创建 filter
```

## 名词解释
```
Queuing discipline: 排队规则，每个网络设备都与一个排队规则相关联。
HTB: Hierarchical Token Bucket, 分层令牌桶
```

## ref
* [Linux-Traffic-Control-Classifier-Action-Subsystem-Architecture.pdf](https://people.netfilter.org/pablo/netdev0.1/papers/Linux-Traffic-Control-Classifier-Action-Subsystem-Architecture.pdf)
* [tc cls_bpf 和 eBPF](https://arthurchiao.art/blog/on-getting-tc-classifier-fully-programmable-zh/#3-tc-cls_bpf-%E5%92%8C-ebpf)
* [深入理解 tc ebpf 的 direct-action (da) 模式](https://arthurchiao.art/blog/understanding-tc-da-mode-zh/#1-%E8%83%8C%E6%99%AF%E7%9F%A5%E8%AF%86linux-%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6tc%E5%AD%90%E7%B3%BB%E7%BB%9F)
* [about-tc](https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/#about-tc)
* [iproute2: tc filter](https://git.kernel.org/pub/scm/network/iproute2/iproute2-next.git/tree/tc/tc_filter.c)