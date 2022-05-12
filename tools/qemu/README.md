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

### 普通用户能正常使用
```
参见 上面
```

## 纯“手工”操作
```
1. Install KVM, Qemu, virt-manager & libvirtd daemon
$ sudo apt install -y qemu qemu-kvm libvirt-daemon libvirt-clients bridge-utils virt-manager

2. Create a virtual machine from the command line
$ sudo virt-install --name u18.04-vm1 --memory 2048 --vcpu 2 --disk path=/home/kvm/images/u18.04-vm1.qcow2,size=50 --cdrom=/home/kvm/os-iso/ubuntu-18.04.5-live-server-amd64.iso --graphics vnc
 说明：
    --name: 虚拟机名称
    --os-type: 操作系统类型
    --os-variant: 操作系统版本
    --vcpu: CPU核数
    --ram: 内存大小(M)
    --disk: 虚拟机镜像路径
    --graphics: 显示设备，此处使用vnc (为了远程方便)
    --network: 网络
2.1 看vnc暴露端口
$ virsh dumpxml u18.04-vm1 |grep vnc
    <graphics type='vnc' port='5900' autoport='yes' listen='127.0.0.1'>

2.2 在本地通过ssh进行端口映射
$ sudo ssh -L 5900:127.0.0.1:5900 root@remote-host

2.3 在本地通过vnc进行配置
```

## 其他
### 显示
```
安装的windows窗口能够自适应
// 下载windows guest tools并安装到agent中
https://www.spice-space.org/download/windows/spice-guest-tools/spice-guest-tools-latest.exe
```

### 其他命令说明
```
# 存储池列表
$ virsh pool-list

# 创建基于目录的存储池
$ mkdir -p /home/kvm/os-iso
$ sudo virsh pool-define-as iso dir --target "/home/kvm/os-iso"
$ sudo virsh pool-build iso
$ sudo virsh pool-start iso
$ sudo virsh pool-autostart iso
$ sudo virsh pool-list
```

## ref
    [install kvm on fedora](https://computingforgeeks.com/how-to-install-kvm-on-fedora/)
    [spice-space](https://www.spice-space.org/download.html)
    [如何使用 virt-manager 运行虚拟机](https://juejin.cn/post/6844903904568672264)
