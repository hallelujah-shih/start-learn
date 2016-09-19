# vpn的简单安装部署
```
为啥需要安装openvpn，懂的
```

## 安装openvpn
```
> yum install epel-release
> yum install openvpn easy-rsa -y
> cp /usr/share/doc/openvpn-x.x.x/sample/sample-config-files/server.conf /etc/openvpn

easy-rsa: Simple shell based CA utility
```

## 创建证书和密钥
```
> mkdir -p /etc/openvpn/easy-rsa/keys
> cp -rf /usr/share/easy-rsa/2.0/* /etc/openvpn/easy-rsa

修改一些变量，使得我们每次生成的时候不用手动修改
vim /etc/openvpn/easy-rsa/vars

export KEY_COUNTRY="CN"
export KEY_PROVINCE="SiChuan"
export KEY_CITY="ChengDu"
export KEY_ORG="start-learn.win"
export KEY_EMAIL="sh19871122@gmail.com"
export KEY_OU="Community"
# X509 Subject Field
export KEY_NAME="server"
export KEY_CN=openvpn.start-learn.win

服务端证书、密钥生成
> cd /etc/openvpn/easy-rsa
> cp openssl-1.0.0.cnf openssl.cnf
> source ./vars
> ./clean-all
# 开始创建ca
> ./build-ca
# 生成服务器的证书和密钥
> ./build-key-server server
# 生成key exchange所用DH算法的文件
> ./build-dh
# 将服务器所用的证书和密钥放入openvpn中
> cd /etc/openvpn/easy-rsa/keys
> cp dh2048.pem ca.key ca.crt server.crt server.key /etc/openvpn

客户端钥匙对生成
> cd /etc/openvpn/easy-rsa
> ./build-key client
```

## 配置openvpn
```
vi /etc/openvpn/server.conf

dh dh2048.pem
push "redirect-gateway def1 bypass-dhcp" # 告诉客户端通过vpn重定向所有流量
# 设置默认DNS服务器
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
# 设置为没有特权的运行
user nobody
group nobody
cipher AES-128-CBC # 自己喜好
port 443 # 最好调整下，用非默认端口，你懂的
proto tcp # 如果网络情况不错，可以选择TCP，当然如果443 UDP也限制了可以设置成tcp，默认UDP即可

cert server.crt
key server.key
```

## 设置路由
```
> yum install iptables-services -y
> systemctl mask firewalld
> systemctl enable iptables
> systemctl stop firewalld
> systemctl start iptables
> iptables --flush

设置转发表
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
iptables-save > /etc/sysconfig/iptables

系统设置允许IP转发
vim /etc/sysctl.conf
net.ipv4.ip_forward = 1
> systemctl restart network.service
```

## 启动openvpn
```
> systemctl -f enable openvpn@server.service
> systemctl start openvpn@server.service

/etc/systemd/system/multi-user.target.wants/openvpn@server.service中详细记录了openvpn的启动，可以在前台启动
```
