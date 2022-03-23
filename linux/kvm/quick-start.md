# kvm

## 包安装
```
sudo dnf -y install libvirt virt-manager libguestfs-tools virt-install

启动服务
sudo systemctl enable --now libvirtd
```

## 纯手动操作

### 创建镜像文件
```
dd if=/dev/zero of=ubuntu18.04.img bs=1M count=8192
# or
qemu-img create ubuntu18.04.img 10G
```

### 启动客户机并使用ISO安装系统
```
qemu-system-x86_64 -m 4G -smp 4 -boot order=cd -hda /root/data/shih/ubuntu18.04.img -cdrom /root/data/os/ubuntu-18.04.5-live-server-amd64.iso
```


## 
