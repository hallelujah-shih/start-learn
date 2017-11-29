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
> rm vmmon-only
> vmware-modconfig –console –install-all
```
