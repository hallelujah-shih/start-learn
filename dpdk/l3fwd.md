# L3FWD程序的分析和结构说明
```
hello world -> l2fwd -> l3fwd的进阶过程
此程序涉及到一些程序逻辑，通过此程序的分析，转入更复杂的程序涉及，作为了解DPVS的基础之一
```

## 结构说明
### 主体结构
```c
// 初始化EAL
rte_eal_init(argc, argv);
// 用户配置分析
parse_args(argc, argv);
//--begin 初始化端口--
for (portid=0; portid<nb_ports; portid++) {
    // 配置以太设备
    rte_eth_dev_configure(portid, nb_rx_queue, n_tx_queue, &port_conf);
    // 获取端口的MAC地址(用于处理转发)
    rte_eth_macaddr_get(portid, &ports_eth_addr[portid]);
    // --begin 初始化内存--
    for (lcore_id=0; lcore_id<RTE_MAX_LCORE; lcore_id++) {
        /* static struct rte_mempool * pktmbuf_pool[NB_SOCKETS]; */
        rte_pktmbuf_pool_create("buf_pool_x", nb_mbuf, MEMPOOL_CACHE_SIZE, 0, RTE_MBUF_DEFAULT_BUF_SIZE, socketid);
        // 并初始化lpm
    }
    // --end 初始化内存--
    // 启动端口传输队列--这儿详情需要看代码，tx与rx是分开启动的
    rte_eth_tx_queue_setup(portid, queueid, queueid, nb_txd, socketid, txconf);
    rte_eth_rx_queue_setup(portid, queueid, nb_rxd, socketid, NULL, pktmbuf_pool[socketid]);
}
//--end 初始化端口--
// 启动所有端口
for (portid=0; portid < nb_ports; portid++) {
    rte_eth_dev_start(portid);
    // 注册回调，对封包做前期处理
    rte_eth_add_rx_callback();
}
// 每个核心上启动处理程序
rte_eal_mp_remote_launch(l3fwd_lkp.main_loop, NULL, CALL_MASTER);```
```

### 关键结构和函数说明
```
说明一些重要的结构和函数逻辑
struct lcore_conf {
    uint16_t n_rx_queue;
    struct lcore_rx_queue rx_queue_list[MAX_RX_QUEUE_PER_LCORE];
    uint16_t n_tx_port;
    uint16_t tx_port_id[RTE_MAX_ETHPORTS];
    uint16_t tx_queue_id[RTE_MAX_ETHPORTS];
    // 每个端口接收数据包的缓存
    struct mbuf_table tx_mbufs[RTE_MAX_ETHPORTS];
    void *ipv4_lookup_struct;
    void *ipv6_lookup_struct;
};/*做了内存对齐*/

struct lcore_rx_queue {
    uint8_t port_id;
    uint8_t queue_id;
};

struct mbuf_table {
    uint16_t len;
    struct rte_mbuf *m_table[MAX_PKT_BURST];
}

NB_MBUF是每个port分配的mbuf pool的元素个数，计算方法为
    RTE_MAX((nb_ports*nb_rx_queue*RTE_TEST_RX_DESC_DEFAULT +
            nb_ports*nb_lcores*MAX_PKT_BURST +
            nb_ports*n_tx_queue*RTE_TEST_TX_DESC_DEFAULT +
            nb_lcores*MEMPOOL_CACHE_SIZE), (unsigned)8192)
    其中RTE_TEST_RX_DESC_DEFAULT为每个接收队列的接收环的大小rte_eth_rx_queue_setup中需要此参数初始化
    其中RTE_TEST_TX_DESC_DEFAULT为每个发送队列的发送环的大小rte_eth_tx_queue_setup中需要此参数初始化
    其中MAX_PKT_BURST表示每次收一串报文的最大值
    其中MEMPOOL_CACHE_SIZE表示每个逻辑核心所单独保留的元素个数，减小对公共池的冲突

l3fwd中的一些元素对应关系
    1. socket:mempool 1:1 // 每个CPU单独对应自己的MEM POOL，设计更合理
    1. port:mempool n:1 // 一般是一个CPU上分配NUM_MBUFS * nb_ports
    2. port:rx/tx queue 1:n 需注意，rx和tx不一定一致
// 说明下，l3fwd的lcore_conf结构定义决定了复杂的初始化过程用
// l3fwd是每个port和lcore绑定的,就出现了每个core就需要分别为每个port创建lcore个数个tx队列
// l3fwd的rx队列依然是每个core配置的，最多MAX_RX_QUEUE_PER_LCORE个{port_id, queue_id}.

其中struct l3fwd_lkp_mode构造了两种类型
    1. exact match(EM),精确匹配
    2. longest prefix match(LPM),最长前缀匹配
    主体分别实现了
        a. setup
        b. check_ptype
        c. cb_parse_ptype
        d. main_loop
        e. get_ipv4_lookup_struct
        f. get_ipv6_lookup_struct

```
