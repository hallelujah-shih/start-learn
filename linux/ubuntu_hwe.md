# 如何在ubuntu中跟进高版本内核升级
```
比如ubuntu 18.04.01内核版本4.15，若只是update & upgrade，那么大版本的内核依然为4.15，而ubuntu 18.04.06的大版本内核已经是5.4了
```

## 安装hwe内核
```
// 18.04桌面版
sudo apt install --install-recommends linux-generic-hwe-18.04 xserver-xorg-hwe-18.04

// 18.04服务器版
sudo apt-get install --install-recommends linux-generic-hwe-18.04

```

## ref
    [ubuntu-hwe-kernel](https://itsfoss.com/ubuntu-hwe-kernel/)
