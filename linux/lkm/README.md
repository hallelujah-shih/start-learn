# lkm学习
```
一些入门小程序
```

## 内核编译
```
ubuntu:
sudo apt-get install vim libncurses5-dev gcc make git exuberant-ctags libssl-dev bison flex libelf-dev bc dwarves zstd git-email

make oldconfig
make -j8
sudo make INSTALL_MOD_STRIP=1 modules_install install

sudo update-initramfs -c -k all
sudo update-grub
```

### 签名
```
若 CONFIG_MODULE_SIG_FORCE=y，则需要签名
否则，虽编译安装成功，但是模块无法使用
若FORCE没有设置，最多标记为"脏模块"

$ cd certs
$ openssl req -new -nodes -utf8 -sha256 -days 36500 -batch -x509 -config x509.genkey -outform PEM -out signing_key.pem -keyout signing_key.pem
```

## hello
```
hello world程序
主要描述了内核模块开发的一些必要东西
```

## REF
* [Kernel Hacking](https://kernelnewbies.org/)
* [Developing on a native Linux platform](https://kernelnewbies.org/OutreachyfirstpatchSetup)
