# FWD_BASIC
```
此处分析转发程序的骨架，是所有程序的基础示例
在example/skeleton
```

## 基本结构
```C
// 初始化EAL
int ret = rte_eal_init(argc, argv);
// 创建mempool
struct rte_mempool *mbuf_pool = rte_pktmbuf_pool_create("MBUF_POOL", NUM_MBUFS * nb_ports, MBUF_CACHE_SIZE, 0, RTE_MBUF_DEFAULT_BUF_SIZE, rte_socket_id());
//----begin 初始化端口-----
// 配置Ether设备
int retval = rte_eth_dev_configure(port, rx_rings, tx_rings, &port_conf);
// 为端口分配并启动RX/TX队列
for (q=0；q<rx_rings; q++) {
    retval = rte_eth_rx_queue_setup(port, q, RX_RING_SIZE, rte_eth_dev_socket_id(port), NULL, mbuf_pool);
}
for (q=0; q<tx_rings; q++) {
    retval = rte_eth_tx_queue_setup(port, q, TX_RING_SIZE, rte_eth_dev_socket_id(port), NULL);
}
// 开启Ether端口
retval = ret_eth_dev_start(port);
//-----end 初始化端口-------
// 包处理逻辑
for (;;) {
    for (port=0; port<nb_ports; port++) {
        // 设置从以太设备接收一串数据包的缓冲区
        struct rte_mbuf *bufs[BURST_SIZE];
        // 从以太设备的接收队列中检索一串输入数据包
        const uint16_t nb_rx = rte_eth_rx_burst(port, 0, bufs, BURST_SIZE);
        if (unlikely(nb_rx == 0))
            continue;
        // 向另外一个端口发送一串收到的报文，port ^ 1巧妙，能保证 0 -> 1 1 > 0 ...
        const uint16_t nb_tx = rte_eth_tx_burst(port ^ 1, 0, bufs, nb_rx);
        // 释放未发送的包
        if (unlikely(nb_tx < nb_rx)) {
            uint16_t buf;
            for (buf = nb_tx; buf < nb_rx; buf++)
                rte_pktmbuf_free(bufs[buf]);
        }
    }
}
```
