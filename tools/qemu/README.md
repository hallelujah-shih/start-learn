# install

## fedora
```
// virtualization packages
sudo dnf -y install bridge-utils libvirt virt-install qemu-kvm

// virtual machine management
sudo dnf -y install libvirt-devel virt-top libguestfs-tools


// daemon
sudo systemctl enable libvirtd
sudo systemctl start libvirtd


// gui manager
sudo dnf -y install virt-manager
```


### 更简单的安装方式
```
sudo dnf install @virtualization
```

### 普通用户能正常使用
```
修改配置文件: /etc/libvirt/libvirtd.conf
将选项放开如下：
unix_sock_group = "libvirt"
unix_sock_rw_perms = "0770"

服务:
sudo systemctl enable libvirtd
sudo systemctl restart libvirtd

用户添加到组:
sudo usermod -a -G libvirt $(whoami)
```

## ubuntu
```
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils

sudo apt install virt-manager
```

## 其他
```
安装的windows窗口能够自适应
// 下载windows guest tools并安装到agent中
https://www.spice-space.org/download/windows/spice-guest-tools/spice-guest-tools-latest.exe
```


## ref
    [install kvm on fedora](https://computingforgeeks.com/how-to-install-kvm-on-fedora/)
    [spice-space](https://www.spice-space.org/download.html)
    [如何使用 virt-manager 运行虚拟机](https://juejin.cn/post/6844903904568672264)
