# ss安装和使用
```
目的，懂的
```

## 地址
[ss](https://github.com/shadowsocks/shadowsocks)

## 搬瓦工
```
vim /etc/security/limits.conf
增加进程能打开的最大句柄数
* soft nofile 51200
* hard nofile 51200

vim /etc/sysctl.conf
增加如下配置
fs.file-max = 51200

net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.netdev_max_backlog = 250000
net.core.somaxconn = 4096

net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 5000
#net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_mem = 25600 51200 102400
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_congestion_control = hybla

执行 sysctl -p
搬瓦工上若出现permission denied on key 'net.nf_conntrack_max'
据说是openvz的模板问题
修复modprobe的：

rm -f /sbin/modprobe 
ln -s /bin/true /sbin/modprobe
修复sysctl的：

rm -f /sbin/sysctl 
ln -s /bin/true /sbin/sysctl
```
## Fedora 27 Shadowsocks+pac
```
Linux上使用SS+PAC相对Win下要麻烦些
```
### Install shadowsocks-qt5
```
> sudo dnf copr enable librehat/shadowsocks
> sudo dnf -y update
> sudo dnf install shadowsocks-qt5
```
### Install genpac
```
# 安装
> sudo pip install genpac
> sudo pip install https://github.com/JinnLynn/genpac/archive/master.zip
# 更新
> pip install --upgrade genpac
> pip install --upgrade https://github.com/JinnLynn/genpac/archive/master.zip
# 卸载
> pip uninstall genpac
# 生成用于socks5
> genpac --format=pac --pac-proxy="SOCKS5 127.0.0.1:1080" --gfwlist-url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt" --user-rule-from=$HOME/user-rules.txt -o $HOME/autoproxy.pac
```
#### genpac user-rule写法
```
! 用户自定义规则语法:
!
!   与gfwlist相同，使用AdBlock Plus过滤规则( http://adblockplus.org/en/filters )
!
!     1. 通配符支持，如 *.example.com/* 实际书写时可省略*为 .example.com/
!     2. 正则表达式支持，以\开始和结束， 如 \[\w]+:\/\/example.com\\
!     3. 例外规则 @@，如 @@*.example.com/* 满足@@后规则的地址不使用代理
!     4. 匹配地址开始和结尾 |，如 |http://example.com、example.com|分别表示以http://example.com开始和以example.com结束的地址
!     5. || 标记，如 ||example.com 则http://example.com、https://example.com、ftp://example.com等地址均满足条件
!     6. 注释 ! 如 ! Comment
!
!   配置自定义规则时需谨慎，尽量避免与gfwlist产生冲突，或将一些本不需要代理的网址添加到代理列表
!
!   规则优先级从高到底为: user-rule > user-rule-from > gfwlist
!
! Tip: 
!   如果生成的是PAC文件，用户定义规则先于gfwlist规则被处理
!   因此可以在这里添加例外或常用网址规则，或能减少在访问这些网址进行查询的时间, 如下面的例子
!
!   但其它格式如wingy, dnsmasq则无此必要, 例外规则将被忽略, 所有规则将被排序
! 

@@sina.com
@@163.com

twitter.com
youtube.com
||google.com
||wikipedia.org
```
### 设置系统代理
```
system settings > network > network proxy;
method: automatic
路径设置为:file:///home/xxx/autoproxy.pac
```
