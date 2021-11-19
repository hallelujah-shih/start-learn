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


## 其他
```
安装的windows窗口能够自适应
// 下载windows guest tools并安装到agent中
https://www.spice-space.org/download/windows/spice-guest-tools/spice-guest-tools-latest.exe
```


## ref
    [install kvm on fedora](https://computingforgeeks.com/how-to-install-kvm-on-fedora/)
    [spice-space](https://www.spice-space.org/download.html)
