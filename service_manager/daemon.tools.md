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

## 安全相关
```
若启动服务失败，可以查看系统相关日志(journalctl)，可以查看audit的日志是否有启动失败相关信息。
若均看到了此消息， setenforce 0之后若看到服务启动成功，在audit中也看到了相关信息，说明和安全相关
这里主要说Selinux
```
### Selinux
``` 
1. 安装管理相关工具
> dnf -y install policycoreutils policycoreutils-python selinux-policy selinux-policy-targeted libselinux-utils setroubleshoot-server setools setools-console mcstrans

2. 检查审计日志
> /var/log/audit/audit.log

3. 最好别这么操作(或者了解下)
先看看
> grep scanboot /var/log/audit/audit.log | audit2allow -m daemontools > daemontools.te
> cat daemontools.te
真正的处理
> grep scanboot /var/log/audit/audit.log | audit2allow -M daemontools
> semodule -i daemontools.pp
```

## reference 
[daemontools](https://cr.yp.to/daemontools.html)
[centos install daemontools](http://marcelog.github.io/articles/install_daemon_tools_centos_amazon_linux.html)
[daemontools auto-start](http://www.phpini.com/linux/rhel-centos-7-setup-daemontools-auto-start)
