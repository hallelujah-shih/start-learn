# 用cgroup-tools libcgroup来管理做控制的示例

## 安装
```
apt install cgroup-tools libcgroup1
```

## 创建服务

### cgconfig
```
# 参见 /usr/share/doc/cgroup-tools/examples/cgconfig.conf
/etc/cgconfig.conf

group 1cpu20limit {
    cpu {
        cpu.cfs_quota_us=10000;
        cpu.cfs_period_us=50000;
    }
}

group dns.slice {
	cpu {
		cpu.shares = 1024;
	}
}
```

### cgrules
```
# 参见 /usr/share/doc/cgroup-tools/examples/cgrules.conf
/etc/cgrules.conf

*:/usr/bin/stress cpu /dns.slice
root:/xxx/main.py      cpu      /1cpu20limit


sudo EDITOR=vim systemctl edit --full cgrules.service

[Unit]
Description=cgroup rules generator
After=network.target cgconfigparser.service

[Service]
User=root
Group=root
Type=forking
PidFile=/var/run/cgrulesengd.pid
EnvironmentFile=-/etc/cgred.conf
ExecStartPre=/usr/sbin/cgconfigparser -l /etc/cgconfig.conf
ExecStart=/usr/sbin/cgrulesengd -s
Restart=always

[Install]
WantedBy=multi-user.target
```

## ref
    [cgroups](https://alikhadivi.medium.com/install-and-config-cgroup-with-cgroupfs-in-ubuntu-cdb9f368ea7c)
