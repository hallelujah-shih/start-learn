# HelloWorld学习
```
DPDK的第一个入门程序解读
```

## 程序结构
```
此程序只有main函数和lcore_hello函数

main函数的主要部分
    1. rte_eal_init(argc, argv) 是常规的DPDK程序的第一步操作,eal的初始化
    2. rte_eal_remote_launch，启动各个核上的线程
    3. rte_eal_mp_wait_lcore，等待线程退出，进行最后的处理
```

## 功能
```
程序先在每个slave core启动执行hello程序，然后再在master core上执行一次hello，并清理资源退出
```
