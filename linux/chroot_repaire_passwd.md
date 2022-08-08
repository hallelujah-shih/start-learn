# chroot修复系统配置、密码等

## 挂载系统盘
```
mount /dev/sdb2 /mnt
```

## 挂载必要文件系统
```
mount -t proc none /mnt/proc
mount -o bind /dev /mnt/dev
mount -o bind /sys /mnt/sys
mount -o bind /run /mnt/run
```

## chroot改变环境
```
chroot /mnt
```

## lvm的情况
```
参见 linux_lvm_mount.md
然后 chroot lvm_dst_path
```

## REF
[How to chroot into a Linux drive](https://www.incredigeek.com/home/how-to-chroot-into-a-linux-drive/)
