# daemontools介绍
```
用于服务管理，和supervisor类似
```

## 安装
```
基于centos7

> wget https://cr.yp.to/daemontools/daemontools-0.76.tar.gz
> tar xzvf daemontools-0.76.tar.gz
# 打patch
> echo gcc -O2 -include /usr/include/errno.h > admin/daemontools-0.76/src/conf-cc
> cd admin/daemontools-0.76/
> package/install
```

## 配置服务
```
# 增加系统自启动服务文件
vim /usr/lib/systemd/system/daemontools.service

[Unit]
Description=daemontools Start supervise
After=sysinit.target

[Service]
Type=simple
User=root
Group=root
Restart=always
ExecStart=/usr/bin/svscanboot /dev/ttyS0
TimeoutSec=0
 
[Install]
WantedBy=multi-user.target

> systemctl enable daemontools
> systemctl start daemontools
```

## 添加服务
```
Centos7 的服务目录在/service

创建sslocal的服务
> mkdir -p /service/ss_local && cd /service/ss_local
vim run

#!/bin/bash

exec setuidgid nobody /usr/bin/sslocal -c /etc/shadowsocks.json

> chmod +x run


创建polipo服务
> mkdir -p /service/polipo && cd /service/polipo
vim run

#!/bin/bash
exec setuidgid nobody /usr/bin/polipo -c /etc/polipo.conf

> chmod +x run
```

## reference 
[daemontools](https://cr.yp.to/daemontools.html)
[centos install daemontools](http://marcelog.github.io/articles/install_daemon_tools_centos_amazon_linux.html)
[daemontools auto-start](http://www.phpini.com/linux/rhel-centos-7-setup-daemontools-auto-start)
