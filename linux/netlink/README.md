# netlink

## 协议基础
```
有三种参见通信模式
1. 用户空间 <--> 内核
2. 用户空间 <--> 用户空间
3. 监听内核多播消息

消息格式如下：
struct nlmsghdr
{
	/** Length of message including header and padding. */
	uint32_t	nlmsg_len;
	/** Message type (content type) */
	uint16_t	nlmsg_type;
	/** Message flags */
	uint16_t	nlmsg_flags;
	/** Sequence number of message \see core_sk_seq_num. */
	uint32_t	nlmsg_seq;
	/** Netlink port */
	uint32_t	nlmsg_pid;
};

mlmsg_type:(各种协议可以自定义消息类型)
    NLMSG_NOOP: 无操作，消息会被丢弃
    NLMSG_ERROR: 错误消息或ACK
    NLMSG_DONE: multipart msg的结尾
    NLMSG_OVERRUN: 超限通知（错误）
    比如rtnetlink协议簇添加了RTM_NEWLINK,RTM_DELLINK等，参见man 7 rtnetlink或(include/uapi/linux/rtnetlink.h)

flags:
    NLM_F_REQUEST: 请求消息
    NLM_F_MULTI: multipart msg
    NLM_F_ACK: 请求ACK消息
    NLM_F_ECHO: 请求回显请求
    其中ECHO与ACK类似，可以与REQUEST组合，得到想要的应答
    下面标志仅仅适用于GET请求
    NLM_F_ROOT: Return based on root of tree.
    NLM_F_MATCH: 返回所有匹配项目
    NLM_F_ATOMIC: 舍弃
    NLM_F_DUMP: 返回所有对象 (NLM_F_ROOT|NLM_F_MATCH).
    下面是与GET互斥的标志
    NLM_F_REPLACE: Replace an existing object if it exists.
    NLM_F_EXCL: Do not update object if it exists already.
    NLM_F_CREATE: Create object if it does not exist yet.
    NLM_F_APPEND: Add object at end of list.

在报文头后面的是有效载荷，Netlink消息的有效载荷是一组使用格式"类型-长度-值"（TLV）表示的属性
Netlink属性头结构nlattr定义如下：
struct nlattr {
    __u16 nla_len;
    __u16 nla_type; (include/net/netlink.h)
}; (include/uapi/linux/netlink.h)
注意：所有的Netlink属性都必须与4字节对齐
```

### NETLINK_ROUTE
### NETLINK_GENERIC(通用Netlink协议)
```
Netlink协议簇的一个缺点是，协议簇数不能超过32(MAX_LINKS)(include/uapi/linux/netlink.h)
这是开发genetlink的主要原因（net/netlink下主要包含af_netlink.c与genetlink.c）(多路复用器)
static int __net_init genl_pernet_init(struct net *net)
{
	struct netlink_kernel_cfg cfg = {
		.input		= genl_rcv,
		.flags		= NL_CFG_F_NONROOT_RECV,
	};

	/* we'll bump the group number right afterwards */
	net->genl_sock = netlink_kernel_create(net, NETLINK_GENERIC, &cfg);

	if (!net->genl_sock && net_eq(net, &init_net))
		panic("GENL: Cannot initialize generic netlink\n");

	if (!net->genl_sock)
		return -ENOMEM;

	return 0;
}

注册控制器簇(genl_ctrl)
static struct genl_family genl_ctrl __ro_after_init = {
	.module = THIS_MODULE,
	.ops = genl_ctrl_ops,
	.n_ops = ARRAY_SIZE(genl_ctrl_ops),
	.mcgrps = genl_ctrl_groups,
	.n_mcgrps = ARRAY_SIZE(genl_ctrl_groups),
	.id = GENL_ID_CTRL,
	.name = "nlctrl",
	.version = 0x2,
	.maxattr = CTRL_ATTR_MAX,
	.policy = ctrl_policy,
	.netnsok = true,
};
err = genl_register_family(&genl_ctrl);

整体通信结构
l0 netlink消息报头(struct nlmsghdr)
l1 gen netlink消息报头(struct genlmsghdr)  (include/uapi/linux/genetlink.h)
l2 用户特定的消息报头（可选）
l3 gen netlink消息有效载荷（可选）
```

## Netlink套接字
```
socket structure(struct nl_sock)
    套接字和所有相关属性
    #include <netlink/socket.h>
    struct nl_sock *nl_socket_alloc(void)
    void nl_socket_free(struct nl_sock *sk)

seq numbers(不同协议可能实现有所不同，根据实际情况使用)
    直接使用计数器
    #include <netlink/socket.h>
    unsigned int nl_socket_use_seq(struct nl_sock *sk);
    但是大多数应用程序不希望自己处理序列号，使用函数nl_send_auto会自动填充seq，并对返回消息进行匹配
    如果所实现协议并为实现seq,可以禁用
    #include <netlink/socket.h>
    void nl_socket_disable_seq_check(struct nl_sock *sk);

Multicast Group Subscriptions(组播订阅)
    2.6.14内核版本前的订阅
    #include <netlink/socket.h>
    void nl_join_groups(struct nl_sock *sk, int bitmask);
    更新的内核:
    #include <netlink/socket.h>
    int nl_socket_add_memberships(struct nl_sock *sk, int group, ...);
    int nl_socket_drop_memberships(struct nl_sock *sk, int group, ...);

Modifiying Socket Callback Configuration
    可以两步操作修改回调
    #include <netlink/socket.h>
    struct nl_cb *nl_socket_get_cb(const struct nl_sock *sk);
    void nl_socket_set_cb(struct nl_sock *sk, struct nl_cb *cb);
    或一次操作完成
    int nl_socket_modify_cb(struct nl_sock *sk, enum nl_cb_type type, enum nl_cb_kind kind, nl_recvmsg_msg_cb_t func, void *arg);

```

## 消息/数据的发送和接收
```
发送消息
    常用函数
    nl_send_auto(nl_send_auto_complete已不推荐seesaw中实现使用的是complete接口)
    nl_send
    nl_send_simple

接收消息
    常用函数
    nl_recvmsgs_default
```

## ref
    [doc](http://www.infradead.org/~tgr/libnl/doc/core.html#core_netlink_fundamentals)
