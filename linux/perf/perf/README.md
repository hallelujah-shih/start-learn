# perf基本使用
```
性能调优基本技能
```

## on-CPU Flame
```
perf record -e cpu-clock -g -p pid1,pid2...
```

## off-CPU Flame
```
Linux可以使用perf和eBPF
```

## Memory

## I/O

## Hot/Cold

## Wakeup

## 其他说明

### 火焰图定义
	* 每个框表示一个函数（一个合并的堆栈帧）
	* Y轴现实堆栈的深度（顶层函数直接指导向了分析事件，它下面的一切都是祖先）
	* X轴横跨样本群，并按照字母排序
	* 框宽度是代表时间比例
	* 每个线程可以合并显示到同一个图中（默认），也可以根据线程分离图
	* 图是可以交互的

