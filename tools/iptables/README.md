# iptables
```
一些IPTABLES的记录
```

## 基本概念
```
```

## 基本使用
```
```
## 其他实例说明
```
```

### 针对SSH作处理
```
设置20秒内允许一个新连接来限制攻击
# requires xt_TARPIT
> iptables -A INPUT -p tcp -m state --state NEW --dport 22 -m recent --update --seconds 20 -j TARPIT
> iptables -A INPUT -p tcp -m state --state NEW --dport 22 -m recent --set -j ACCEPT
下面例子中
* 第一条规则允许每小时最多2个连接，在达到每小时2个连接的限制后，第二个规则变为活动状态，并且hashlimit模块从1分钟(60 000毫秒)开始倒计时(/proc/net/ipt_hashlimit/$hashlimit-name)。如果您在1分钟内连接，则hashlimit计数器将重置为60秒。如果您在1分钟后连接，则会跳到第三个规则并允许访问。
# requires hashlimit
> iptables -A INPUT -p tcp -m tcp --dport 22 -m state --state NEW -m hashlimit --hashlimit 1/hour --hashlimit-burst 2 --hashlimit-mode srcip --hashlimit-name SSH --hashlimit-htable-expire 60000 -j ACCEPT
> iptables -A INPUT -p tcp -m tcp --dport 22 --tcp-flags SYN,RST,ACK SYN -j DROP
> iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
```

## REF
    [filter for SSH brute-force]("http://mikhailian.mova.org/node/147")
    [How does iptables hashlimit module work?]("http://tlfabian.blogspot.com/2014/06/how-does-iptables-hashlimit-module-work.html")
    [Understanding iptable’s hashlimit module](http://poorlydocumented.com/2017/08/understanding-iptables-hashlimit-module/)
    [How To List and Delete Iptables Firewall Rules](https://www.digitalocean.com/community/tutorials/how-to-list-and-delete-iptables-firewall-rules)
