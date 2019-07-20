# linux mount lvm volume
```
挂在lvm，读取老系统中的数据
```

## 安装 lvm
```
sudo dnf install lvm2
```

## 查找lvm设备
```
sudo vgscan

ex output:
  Reading volume groups from cache.
  Found volume group "fedora" using metadata type lvm2
  Found volume group "old_system" using metadata type lvm2
```

## 启用
```
sudo vgchange -ay
or 
sudo vgchange -ay "old_system"
````

## 查看
```
sudo lvdisplay
or
sudo lvs

ex output:
  LV   VG         Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home fedora     -wi-ao---- <23.33g
  root fedora     -wi-ao---- <47.78g
  swap fedora     -wi-ao----   7.89g
  home old_system -wi-a----- 179.85g
  root old_system -wi-a-----  50.00g
  swap old_system -wi-a-----   7.62g
```

## 挂载目录
```
sudo mount /dev/old_system/home /mnt/
```
