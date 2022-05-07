# netfilter
```C
一些基本知识

netfilter的表和链，表(table)是根据“用来做什么”的标准来组织的，其中优先级的定义如下
<include/uapi/linux/netfilter_ipv4.h>
enum nf_ip_hook_priorities {
	NF_IP_PRI_FIRST = INT_MIN,
	NF_IP_PRI_RAW_BEFORE_DEFRAG = -450,
	NF_IP_PRI_CONNTRACK_DEFRAG = -400,
	NF_IP_PRI_RAW = -300,
	NF_IP_PRI_SELINUX_FIRST = -225,
	NF_IP_PRI_CONNTRACK = -200,
	NF_IP_PRI_MANGLE = -150,
	NF_IP_PRI_NAT_DST = -100,
	NF_IP_PRI_FILTER = 0,
	NF_IP_PRI_SECURITY = 50,
	NF_IP_PRI_NAT_SRC = 100,
	NF_IP_PRI_SELINUX_LAST = 225,
	NF_IP_PRI_CONNTRACK_HELPER = 300,
	NF_IP_PRI_CONNTRACK_CONFIRM = INT_MAX,
	NF_IP_PRI_LAST = INT_MAX,
};
由上亦可知，RAW > CONNTRACK > MANGLE > DNAT > FILTER > SNAT
```

## 链(chains)
```C
<linux/uapi/netfilter.h>
enum nf_inet_hooks {
	NF_INET_PRE_ROUTING,
	NF_INET_LOCAL_IN,
	NF_INET_FORWARD,
	NF_INET_LOCAL_OUT,
	NF_INET_POST_ROUTING,
	NF_INET_NUMHOOKS,
	NF_INET_INGRESS = NF_INET_NUMHOOKS,
};

PREROUTING  <-> NF_INET_PRE_ROUTING
INPUT       <-> NF_INET_LOCAL_IN
FORWARD     <-> NF_INET_FORWARD
OUTPUT      <-> NF_INET_LOCAL_OUT
POSTROUTING <-> NF_INET_POST_ROUTING
```

## 表(tables)
```
表根据用来做什么的标准进行了组织
```

### table-raw
```C
raw表主要只用于一件事，那就是在数据包上设置一个标记，它们不应该被连接跟踪系统处理。这是通过在数据包上使用 NOTRACK 目标来完成的。如果一个连接被 NOTRACK 目标命中，那么 conntrack 将根本不跟踪该连接。

<net/ipv4/netfilter/iptable_raw>
#define RAW_VALID_HOOKS ((1 << NF_INET_PRE_ROUTING) | (1 << NF_INET_LOCAL_OUT))

static const struct xt_table packet_raw = {
	.name = "raw",
	.valid_hooks =  RAW_VALID_HOOKS,
	.me = THIS_MODULE,
	.af = NFPROTO_IPV4,
	.priority = NF_IP_PRI_RAW,
};

由上代码可知，有效链为NF_INET_PRE_ROUTING和NF_INET_LOCAL_OUT，不管入和出，都在连接跟踪前处理
```

### table-mangle
```C
mangle表应该主要用于处理数据包。换句话说，您可以自由地使用此表中的 mangle 目标，来更改 TOS（服务类型）字段等。
 * 不要使用此表进行任何过滤；任何 DNAT、SNAT 或伪装也不会在此表中起作用。
 以下targets只在mangle表中有效：
	* TOS
	* MARK： 设置标记，而后可以根据数据包的标记进行不同的路由或者做其他的策略，如QoS
	* SECMARK
	* CONNSECMARK
	* TTL

<net/ipv4/netfilter/iptale_mangle.c>
#define MANGLE_VALID_HOOKS ((1 << NF_INET_PRE_ROUTING) | \
			    (1 << NF_INET_LOCAL_IN) | \
			    (1 << NF_INET_FORWARD) | \
			    (1 << NF_INET_LOCAL_OUT) | \
			    (1 << NF_INET_POST_ROUTING))

static const struct xt_table packet_mangler = {
	.name		= "mangle",
	.valid_hooks	= MANGLE_VALID_HOOKS,
	.me		= THIS_MODULE,
	.af		= NFPROTO_IPV4,
	.priority	= NF_IP_PRI_MANGLE,
};
从代码可知，mangle表的有效链包括NF_INET_PRE_ROUTING，NF_INET_LOCAL_IN，NF_INET_FORWARD，NF_INET_LOCAL_OUT，NF_INET_POST_ROUTING
```

### table-nat
```C
nat表用于对IP包进行NAT转换
target:
	* DNAT: 主要用于您拥有公共 IP 并希望将对防火墙的访问重定向到其他主机（例如在 DMZ 上）的情况。换句话说，我们改变了数据包的目的地址并将其重新路由到主机。
	* SNAT: 主要用于改变数据包的源地址。在大多数情况下，你会隐藏你的本地网络或DMZ等。
	* MASQUERADE: 使用方法与 SNAT 完全相同， 但需要多花一点时间来计算。原因是每次数据包hit时，它都会自动检查要使用的IP地址， 而不是像SNAT目标那样--只使用单一配置的IP地址。（动态分配的地址处理方便）
	* REDIRECT

<net/ipv4/netfilter/iptable_nat.c>
static const struct xt_table nf_nat_ipv4_table = {
	.name		= "nat",
	.valid_hooks	= (1 << NF_INET_PRE_ROUTING) |
			  (1 << NF_INET_POST_ROUTING) |
			  (1 << NF_INET_LOCAL_OUT) |
			  (1 << NF_INET_LOCAL_IN),
	.me		= THIS_MODULE,
	.af		= NFPROTO_IPV4,
};

static const struct nf_hook_ops nf_nat_ipv4_ops[] = {
	{
		.hook		= ipt_do_table,
		.pf		= NFPROTO_IPV4,
		.hooknum	= NF_INET_PRE_ROUTING,
		.priority	= NF_IP_PRI_NAT_DST,
	},
	{
		.hook		= ipt_do_table,
		.pf		= NFPROTO_IPV4,
		.hooknum	= NF_INET_POST_ROUTING,
		.priority	= NF_IP_PRI_NAT_SRC,
	},
	{
		.hook		= ipt_do_table,
		.pf		= NFPROTO_IPV4,
		.hooknum	= NF_INET_LOCAL_OUT,
		.priority	= NF_IP_PRI_NAT_DST,
	},
	{
		.hook		= ipt_do_table,
		.pf		= NFPROTO_IPV4,
		.hooknum	= NF_INET_LOCAL_IN,
		.priority	= NF_IP_PRI_NAT_SRC,
	},
};
由上面代码可知，nat的有效链包括: NF_INET_PRE_ROUTING, NF_INET_POST_ROUTING, NF_INET_LOCAL_OUT, NF_INET_LOCAL_IN

也可知，在NF_INET_PRE_ROUTING的时候执行DNAT，NF_INET_LOCAL_IN的时候执行SNAT，在NF_INET_LOCAL_OUT的时候执行	DNAT，NF_INET_POST_ROUTING的时候执行SNAT
```

### table-filter
```C
filter表用于对数据包的过滤

<net/ipv4/netfilter/iptable_filter.c>
#define FILTER_VALID_HOOKS ((1 << NF_INET_LOCAL_IN) | \
			    (1 << NF_INET_FORWARD) | \
			    (1 << NF_INET_LOCAL_OUT))

static const struct xt_table packet_filter = {
	.name		= "filter",
	.valid_hooks	= FILTER_VALID_HOOKS,
	.me		= THIS_MODULE,
	.af		= NFPROTO_IPV4,
	.priority	= NF_IP_PRI_FILTER,
};
从上面的代码可知，filter表的有效链为INPUT，OUTPUT，FORWARD
```

## 状态机
```
在 iptables 中，数据包可以与处于四种不同所谓状态的跟踪连接相关联。分别为NEW、ESTABLISHED、RELATED、INVALID。通过 --state 匹配，我们可以轻松控制允许谁或什么启动新会话。

所有的连接跟踪都是由内核中称为 conntrack 的特殊框架完成的。除了在 OUTPUT 链中处理的本地生成的数据包外，所有连接跟踪都在 PREROUTING 链中处理。当我们向外发起连接时，OUTPUT链中将状态设置为NEW，我们收到回应数据包时，在PREROUTING链中将状态更改为ESTABLISHED；当我们收到连接请求时，在PREROUTING链中将状态设置为NEW。
```

### 状态说明
```
NEW: 该数据包是我们看到的第一个数据包。这意味着conntrack模块看到的第一个数据包，在一个特定的连接中，将被匹配。例如，如果我们看到一个SYN数据包，它是我们看到的连接中的第一个数据包，它将被匹配。然而，该数据包可能不是SYN数据包，但仍然被认为是新的。这在某些情况下可能会导致某些问题，但当我们需要从其他防火墙中拾取丢失的连接时，或者当一个连接已经超时，但实际上没有关闭时，它也可能是非常有用的。
	* 注意是第一个包，与是否为SYN没关系

ESTABLISHED: 已经看到了两个方向的流量，然后将持续匹配这些数据包。ESTABLISHED连接是相当容易理解的。进入ESTABLISHED状态的唯一要求是，一台主机发送了一个数据包，随后从另一台主机得到一个回复。NEW将在收到回复数据包后或通过防火墙改变为ESTABLISHED状态。如果我们创建了一个数据包，反过来产生了回复的ICMP消息，那么ICMP回复消息也可以被认为是ESTABLISHED。

RELATED: 是一个比较棘手的状态。当一个连接与另一个已经建立的连接相关时，它就被认为是RELATED。这意味着，要使一个连接被认为是RELATED，我们必须首先有一个被认为是ESTABLISHED的连接。这个ESTABLISHED连接将在主连接之外产生一个连接。如果conntrack模块能够理解这个连接是RELATED，那么这个新产生的连接将被认为是RELATED。一些可以被认为是RELATED连接的好例子:FTP-data的连接被认为与FTP的控制端口有RELATED关系；以及通过IRC发出的DCC连接。

INVALID: 意味着数据包无法被识别，或者它没有任何状态。这可能是由于几个原因，如系统内存耗尽或ICMP错误信息不响应任何已知连接。一般来说，在这种状态下应该DROP。

UNTRACKED: 一个数据包在原始表中被标记为NOTRACK目标，那么这个数据包在状态机中就会显示为UNTRACKED。这也意味着所有相关的连接都不会被看到，所以在处理UNTRACKED连接时必须谨慎，因为状态机将无法看到相关的ICMP消息等。
```

## iptables matches
```
generic matches: 可用于所有规则
TCP matches: 应用于TCP包
UDP matches: 应用于UDP包
ICMP matches: 应用于ICMP包
special matches: 如state等，应用于限定的matches

显式匹配是必须使用 -m 或 --match 选项专门加载的匹配。
```

### generic matches
| matches                  | example                                                              | desc                                                        |
| ------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| -p, --protocol           | iptables -A INPUT -p tcp                                             | 协议匹配，可以是tcp,udp等,也可以用/etc/protocols文件中描述的数值来表示              |
| -s, --src, --source      | iptables -A INPUT -s 192.168.1.1；iptables -A INPUT -s 192.168.0.0/24 | src ip，可以使用单个IP，也可以使用CIDR表示的网段                              |
| -d, --dst, --destination | iptables -A INPUT -d 192.168.1.1                                     | 参见source                                                    |
| -i, --in-interface       | iptables -A INPUT -i eth0                                            | 此匹配只在INPUT,FORWARD,PREROUTING链中合法，可以 -i ! eth0表示除了eth0以外的应用 |
| -o, --out-interface      | iptables -A FORWARD -o eth0                                          | 参见--in-interface                                            |
| -f, --fragment           | iptables -A INPUT -f                                                 | 分片匹配                                                        |


### TCP matches(隐式匹配)
| matches                     | example                                     | desc                                                                                         |
| --------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------- |
| --sport, --source-port      | iptables -A INPUT -p tcp --sport 22         | 匹配源端口，--source-port 22:80表示22到80的端口，--source-port ：80表示0到80的端口，--source-port 22: 表示大于22的所有端口 |
| --dport, --destination-port | iptables -A INPUT -p tcp --dport 22         | 参见--source-port                                                                              |
| --tcp-flags                 | iptables -p tcp --tcp-flags SYN,FIN,ACK SYN |                                                                                              |
| --syn                       | iptables -p tcp --syn                       | 旧时代的遗留，与--tcp-flags SYN,RST,ACK SYN 匹配完全相同                                                   |
| --tcp-option                | iptables -p tcp --tcp-option 16             | 对TCP option进行匹配                                                                              |

### UDP matches(隐式匹配)
| matches                     | example                                     | desc                                       |
| --------------------------- | ------------------------------------------- | ------------------------------------------ |
| --sport, --source-port      | iptables -A INPUT -p udp --sport 53         | 参见前文--source-port                          |
| --dport, --destination-port | iptables -A INPUT -p udp --dport 53         | 参见--source-port                            |

### ICMP matches(隐式匹配)
| matches                     | example                                     | desc                                       |
| --------------------------- | ------------------------------------------- | ------------------------------------------ |
| --icmp-type                 | iptables -A INPUT -p icmp --icmp-type 8     | icmp类型匹配                                   |

### SCTP matches(隐式匹配)
| matches                     | example                                                    | desc                                       |
| --------------------------- | ---------------------------------------------------------- | ------------------------------------------ |
| --source-port, --sport      | iptables -A INPUT -p sctp --source-port 80                 |                                            |
| --destination-port, --dport | iptables -A INPUT -p sctp --destination-port 80            |                                            |
| --chunk-types               | iptables -A INPUT -p sctp --chunk-types any INIT,INIT_ACK  |                                            |

### Addrtype match(显式，地址类匹配)
```
地址类型包括：
ANYCAST： 这是一种一对多的关联连接类型，其中只有一个接收器主机实际接收数据
BLACKHOLE： 黑洞地址将简单地删除数据包并且不发送任何回复
BROADCAST： 广播数据包是以一对多关系发送给特定网络中每个人的单个数据包
LOCAL： 我们正在处理的主机的本地地址。例如 127.0.0.1。
MULTICAST
NAT： 被内核NAT的地址
PROHIBIT： 与 blackhole 相同，只是会生成一个禁止的答案，在 IPv4 情况下，这意味着将生成ICMP 通信禁止。
THROW： Linux内核中的特殊路由。如果在路由表中抛出一个数据包，它将表现得好像在表中没有找到路由一样。在正常路由中，这意味着数据包的行为就像没有路由一样。在策略路由中，可能会在另一个路由表中找到另一个路由。

UNICAST： 单个地址的真实可路由地址。最常见的路线类型。
UNREACHABLE： 无法到达的地址。数据包将被丢弃，并且将生成一个ICMP 主机不可达
UNSPEC： 没有实际意义的未指定地址。
XRESOLVE： 
```
| matches    | example                                          | desc                                         |
| ---------- | ------------------------------------------------ | -------------------------------------------- |
| --src-type | iptables -A INPUT -m addrtype --src-type UNICAST | 匹配地址类型，可以用逗号隔开--src-type BROADCAST,MULTICAST |
| --dst-type | iptables -A INPUT -m addrtype --dst-type UNICAST | 参见上面                                         |

### AH/ESP match
```
略
```

### Comment match
| matches    | example                                            | desc |
| ---------- | -------------------------------------------------- | ---- |
| --comment  | iptables -A INPUT -m comment --comment "A comment" | 添加注释 |

### Connmark match
```
connmark match与mark match在MARK/mark组合匹配非常相似。connmark match用于匹配已CONNMARK目标的连接上设置的标记。它只需要一个选项。
```
| matches    | example                                           | desc       |
| ---------- | ------------------------------------------------- | ---------- |
| --mark     | iptables -A INPUT -m connmark --mark 12 -j ACCEPT | 设置connmark |

### Conntrack match
```
conntrack match是state match的扩展，可以更精细化的方式匹配数据包。
```
| matches     | example                                                          | desc                                                                 |
| ----------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- |
| --ctstate   | iptables -A INPUT -p tcp -m conntrack --ctstate RELATED          | 根据conntrack状态匹配数据包状态,可用状态为：INVALID，ESTABLISHED，NEW，RELATED，SNAT，DNAT |
| --ctproto   | iptables -A INPUT -p tcp -m conntrack --ctproto TCP              | 匹配协议，与--protocol等同                                                   |
| --ctorigsrc | iptables -A INPUT -p tcp -m conntrack --ctorigsrc 192.168.0.0/24 |                                                                      |
| --ctorigdst | iptables -A INPUT -p tcp -m conntrack --ctorigdst 192.168.0.0/24 |                                                                      |
| --ctreplsrc | iptables -A INPUT -p tcp -m conntrack --ctreplsrc 192.168.0.0/24 |                                                                      |
| --ctrepldst | iptables -A INPUT -p tcp -m conntrack --ctrepldst 192.168.0.0/24 |                                                                      |
| --ctstatus  | iptables -A INPUT -p tcp -m conntrack --ctstatus RELATED         | 可用状态：NONE，EXPECTED，SEEN_REPLY，ASSURED                                |
| --ctexpire  | iptables -A INPUT -p tcp -m conntrack --ctexpire 100:150         |                                                                      |

### Dscp match
| matches      | example                                                          | desc                                   |
| ------------ | ---------------------------------------------------------------- | -------------------------------------- |
| --dscp       | iptables -A INPUT -p tcp -m dscp --dscp 32                       |                                        |
| --dscp-class | iptables -A INPUT -p tcp -m dscp --dscp-class BE                 |                                        |

### Ecn match
| matches       | example                                                          | desc                                   |
| ------------- | ---------------------------------------------------------------- | -------------------------------------- |
| --ecn         | iptables -A INPUT -p tcp -m ecn --ecn-tcp-cwr                    |                                        |
| --ecn-tcp-ece | iptables -A INPUT -p tcp -m ecn --ecn-tcp-ece                    |                                        |
| --ecn-ip-ect  | iptables -A INPUT -p tcp -m ecn --ecn-ip-ect 1                   |                                        |

### Hashlimit match
| matches                       | example                                                                                                                                                           | desc |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| --hashlimit                   | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000/sec --hashlimit-mode dstip,dstport --hashlimit-name hosts                                |      |
| --hashlimit-mode              | iptables -A INPUT -p tcp --dst 192.168.0.0/16 -m hashlimit --hashlimit 1000/sec --hashlimit-mode dstip --hashlimit-name hosts                                     |      |
| --hashlimit-name              | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts                                    |      |
| --hashlimit-burst             | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts --hashlimit-burst 2000             |      |
| --hashlimit-htable-size       | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts --hashlimit-htable-size 500        |      |
| --hashlimit-htable-max        | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts --hashlimit-htable-max 500         |      |
| --hashlimit-htable-gcinterval | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts --hashlimit-htable-gcinterval 1000 |      |
| --hashlimit-htable-expire     | iptables -A INPUT -p tcp --dst 192.168.0.3 -m hashlimit --hashlimit 1000 --hashlimit-mode dstip,dstport --hashlimit-name hosts --hashlimit-htable-expire 10000    |      |

### IP range match
| matches                       | example                                                                   | desc |
| ----------------------------- | ------------------------------------------------------------------------- | ---- |
| --src-range                   | iptables -A INPUT -p tcp -m iprange --src-range 192.168.1.13-192.168.2.19 |      |
| --dst-range                   | iptables -A INPUT -p tcp -m iprange --dst-range 192.168.1.13-192.168.2.19 |      |

### Length match
| matches                       | example                                               | desc |
| ----------------------------- | ----------------------------------------------------- | ---- |
| --length                      | iptables -A INPUT -p tcp -m length --length 1400:1500 |      |

### Limit match
| matches                       | example                                    | desc |
| ----------------------------- | ------------------------------------------ | ---- |
| --limit                       | iptables -A INPUT -m limit --limit 3/hour  |      |
| --limit-burst                 | iptables -A INPUT -m limit --limit-burst 5 |      |

### Mac match
| matches                       | example                                                 | desc |
| ----------------------------- | ------------------------------------------------------- | ---- |
| --mac-source                  | iptables -A INPUT -m mac --mac-source 00:00:00:00:00:01 |      |

### Mark match
| matches                       | example                                      | desc |
| ----------------------------- | -------------------------------------------- | ---- |
| --mark                        | iptables -t mangle -A INPUT -m mark --mark 1 |      |

### Multiport match
| matches                       | example                                                               | desc |
| ----------------------------- | --------------------------------------------------------------------- | ---- |
| --source-port                 | iptables -A INPUT -p tcp -m multiport --source-port 22,53,80,110      |      |
| --destination-port            | iptables -A INPUT -p tcp -m multiport --destination-port 22,53,80,110 |      |
| --port                        | iptables -A INPUT -p tcp -m multiport --port 22,53,80,110             |      |

### Owner match
| matches                       | example                                       | desc |
| ----------------------------- | --------------------------------------------- | ---- |
| --cmd-owner                   | iptables -A OUTPUT -m owner --cmd-owner httpd |      |
| --uid-owner                   | iptables -A OUTPUT -m owner --uid-owner 500   |      |
| --gid-owner                   | iptables -A OUTPUT -m owner --gid-owner 0     |      |
| --pid-owner                   | iptables -A OUTPUT -m owner --pid-owner 78    |      |
| --sid-owner                   | iptables -A OUTPUT -m owner --sid-owner 100   |      |

### Packet type match
| matches                       | example                                          | desc |
| ----------------------------- | ------------------------------------------------ | ---- |
| --pkt-type                    | iptables -A OUTPUT -m pkttype --pkt-type unicast |      |

### Realm match
| matches                       | example                                     | desc |
| ----------------------------- | ------------------------------------------- | ---- |
| --realm                       | iptables -A OUTPUT -m realm --realm 4       |      |

### Recent match
```
略过，太复杂
```

### State match
| matches                       | example                                                | desc |
| ----------------------------- | ------------------------------------------------------ | ---- |
| --state                       | iptables -A INPUT -m state --state RELATED,ESTABLISHED |      |

### Tcpmss match
| matches                       | example                                                                        | desc |
| ----------------------------- | ------------------------------------------------------------------------------ | ---- |
| --mss                         | iptables -A INPUT -p tcp --tcp-flags SYN,ACK,RST SYN -m tcpmss --mss 2000:2500 |      |

### Tos match
| matches                       | example                                     | desc |
| ----------------------------- | ------------------------------------------- | ---- |
| --tos                         | iptables -A INPUT -p tcp -m tos --tos 0x16  |      |


### Ttl match
| matches                       | example                                     | desc |
| ----------------------------- | ------------------------------------------- | ---- |
| --ttl-eq                      | iptables -A OUTPUT -m ttl --ttl-eq 60       |      |
| --ttl-gt                      | iptables -A OUTPUT -m ttl --ttl-gt 64       |      |
| --ttl-lt                      | iptables -A OUTPUT -m ttl --ttl-lt 64       |      |


## targets and jumps(目标和跳转)

### ACCEPT target
```
一旦ACCEPT作为target，那么不会继续同一个链中的其他规则
```

### CLASSIFY target
```
用于数据包分配，提供几个不同的qdisc(队列规则)使用；仅在mangle表的POSTROUTING链中有效。

ex:
	iptables -t mangle -A POSTROUTING -p tcp --dport 80 -j CLASSIFY --set-class 20:10
```

### CLUSTERIP target

### CONNMARK target
```
用于在整个连接上设置标记，与 MARK target的方式非常相似，可以与 connmark match 一起使用，以匹配将来的连接。假设我们在标头中看到特定模式，我们不想只标记那个数据包，而是整个连接。在这种情况下，CONNMARK target是一个完美的解决方案。

能用于所有链和表，注意NAT，需要查文档

ex:
	iptables -t nat -A PREROUTING -p tcp --dport 80 -j CONNMARK --set-mark 4
```

### CONNSECMARK target

### DNAT target

### DROP target
```
更友好的做法是使用REJECT target
```

### DSCP target

### ECN target

### LOG target options

### MARK target
```
为特定包设置netfilter标记的；只能用于mangle表
```

### MASQUERADE target

### MIRROR target

### NETMAP target

### NFQUEUE target

### NOTRACK target

### QUEUE target

### REDIRECT target

### REJECT target

### RETURN target

### SAME target

### SECMARK target

### SNAT target

### TCPMSS target

### TOS target

### TTL target

### ULOG target

## ref
	[iptables-tutorial](https://book.huihoo.com/iptables-tutorial/)