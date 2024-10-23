# 通过tailscale和headscale组网
```
Tailscale是建立在Wireguard之上的VPN。Wireguard本身是基于UDP的点对点VPN，通过headscale+tailscale可以实现subnet间的通信。

而Headscale则是作为一个开源的控制服务器，为Tailscale网络中节点之间的Wireguard公钥交换点工作。它为客户端分配IP地址，创建每个用户之间的边界，允许用户之间共享机器，并暴露您的节点宣传的路由。
```

## 安装headscale
```
选择一个服务端部署

安装二进制：
curl -fL https://github.com/juanfont/headscale/releases/download/v0.23.0/headscale_0.23.0_linux_amd64 -o /usr/bin/headscale
chmod +x /usr/bin/headscale

处理配置：
mkdir -p /etc/headscale /var/lib/headscale

useradd \
  --create-home \
  --home-dir /var/lib/headscale/ \
  --system \
  --user-group \
  --shell /usr/sbin/nologin \
  headscale

curl -fL https://github.com/juanfont/headscale/raw/main/config-example.yaml -o /etc/headscale/config.yaml

根据自己需求修改配置文件： /etc/headscale/config.yaml


处理服务自启动：
curl -fL https://github.com/juanfont/headscale/blob/main/docs/packaging/headscale.systemd.service -o /etc/systemd/system/headscale.service

systemctl daemon-reload
systemctl enable headscale
systemctl start headscale
```

## 安装tailscale
```
在每个客户端节点上安装（linux,windows的自己找，android的应用商店下）：
curl -fsSL https://tailscale.com/install.sh | sh
```

## 打通子网
```
边缘节点配置（linux）：
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf
sudo iptables -t mangle -A FORWARD -o tailscale0 -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu

iptables的操作可以固化到service的配置中，如下：
ExecStartPost=/usr/sbin/iptables -t mangle -A FORWARD -o tailscale0 -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
ExecStopPost=/usr/sbin/iptables -t mangle -D FORWARD -o tailscale0 -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu

systemctl daemon-reload

宣告网段：
sudo tailscale up --login-server=https://my-headscale-domain.com --accept-routes=true --accept-dns=true --advertise-routes=192.168.10.0/24

在服务器上执行：
headscale routes list
选择需要暴露的子网，比如此处ID是2
headscale routes enable -r 2

在需要访问此子网的客户端上执行：
sudo tailscale up --login-server=https://my-headscale-domain.com --accept-routes=true --accept-dns=true
即可访问
```

## ref
[headscale](https://github.com/juanfont/headscale)
