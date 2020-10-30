# 此处记录了一些VMware的问题解决
## Linux下问题汇聚
### 问题1，提示内存不足
```
内核版本:4.13
vmware版本:14
> su -
> cd /usr/lib/vmware/modules/source
> tar xf vmmon.tar
> wget https://raw.githubusercontent.com/mkubecek/vmware-host-modules/fadedd9c8a4dd23f74da2b448572df95666dfe12/vmmon-only/linux/hostif.c
> mv hostif.c vmmon-only/linux/hostif.c
> rm vmmon.tar
> tar cf vmmon.tar vmmon-only
> rm vmmon-only -rf
> vmware-modconfig –console –install-all
```

### 升级openssh后ssh连接报错
```
fedora 29
packet_write_wait: Connection to xxxxxx port xx: Broken pipe
细节未追究，大概是vmware nat的锅
在config中加入
Host *
    IPQoS lowdelay throughput
问题得到解决
```

### vmware.service启动错误
```
https://askbot.fedoraproject.org/en/question/109763/installing-vmware-1257-for-linux-on-fedora-26/
https://kb.vmware.com/s/article/58533
https://kb.vmware.com/s/article/2146460
```
