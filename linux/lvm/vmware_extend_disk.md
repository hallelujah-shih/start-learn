# vmware扩容
```
系统是Fedora31
```

## vmware虚拟机中磁盘选项中增加你想要的磁盘大小

## fdisk磁盘分区

## 格式化
```
我机器文件使用的是ext4格式，设备为sda3

mkfs -t ext4 /dev/sdb3
```

## 创建PV
```
1. 更新内核的分区信息（不用reboot）
> partprobe
> pvcreate /dev/sda3
> pvscan
```

## 查看LV的信息
```
# 此处的root是我扩展后的，若本身没有扩展，按需扩展即可
> sudo lvdisplay
    --- Logical volume ---
  LV Path                /dev/fedora/swap
  LV Name                swap
  VG Name                fedora
  LV UUID                kP1gJ2-Al6e-EhT6-4zaz-lMkQ-Oy5p-okkDRQ
  LV Write Access        read/write
  LV Creation host, time localhost, 2019-07-21 03:23:04 +0800
  LV Status              available
  # open                 2
  LV Size                7.89 GiB
  Current LE             2020
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1

  --- Logical volume ---
  LV Path                /dev/fedora/home
  LV Name                home
  VG Name                fedora
  LV UUID                b0Y5Wr-Kxdp-ATCJ-L0yc-mKe2-306P-dRSqOw
  LV Write Access        read/write
  LV Creation host, time localhost, 2019-07-21 03:23:04 +0800
  LV Status              available
  # open                 1
  LV Size                <23.33 GiB
  Current LE             5972
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2

  --- Logical volume ---
  LV Path                /dev/fedora/root
  LV Name                root
  VG Name                fedora
  LV UUID                aRauWe-TyR5-yjgR-o1mm-xCrv-4j3d-O3mi8i
  LV Write Access        read/write
  LV Creation host, time localhost, 2019-07-21 03:23:08 +0800
  LV Status              available
  # open                 1
  LV Size                127.77 GiB
  Current LE             32710
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0

```
## PV加入VG组
```
我的设备是/dev/sda3，根据上面lv的信息可知vg的name是fedora
> sudo vgextend fedora /dev/sda3
```

## 逻辑卷扩展
```
根据lvdisplay的结果，我需要扩展的逻辑卷是root，路径为/dev/fedora/root，并将所有空间扩展至此卷
> sudo lvextend /dev/fedora/root -l+100%FREE
```

## 调整分区大小
```
我使用的ext4，所以使用命令resize2fs
> sudo resize2fs /dev/fedora/root
```
