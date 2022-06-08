# rebuild ubuntu pkg

## 准备目录
```
    安装devscripts包，包含许多debian源包的有用工具
    apt install build-essential fakeroot devscripts

    修改/etc/apt/sources.list，放开deb-src

    准备目录
    mkdir -p src/debian/
    chown -Rv _apt:root src
    chmod -Rv 700 src
    cd src/debian
```

## 准备源码以及编译依赖
````
    安装依赖以及下载source包
    apt build-dep python3.6
    apt source python3.6

    # option 若source文件修改错了，可以通过dpkg-source -x xxxx.dsc来重新生成source目录

    目录下将会有如下目录和文件:
        目录： python3.6-3.6.9
        文件： python3.6_3.6.9-1~18.04ubuntu1.4.dsc
        包：   python3.6_3.6.9-1~18.04ubuntu1.4.debian.tar.xz、python3.6_3.6.9.orig.tar.xz

    cd python3.6-3.6.9
    修改规则debian/rules文件，如增加python支持usdt
    打开debian/rules，并在common_configure_args下面增加选项--with-dtrace，保存并执行如下命令
    debuild -us -uc

    ex: iptables-1.6.1支持ebpf的object pinned
        apt build-dep iptables
        apt source iptables
        
        cd iptables-1.6.1
        vim debian/rules:
            override_dh_auto_build:
                make CFLAGS="-g -O2 -include /usr/include/linux/unistd.h"

        # 重新编译
        debuild -us -uc
        cp extensions/libxt_bpf.so /usr/lib/x86_64-linux-gnu/xtables/libxt_bpf.so

    安装
    dpkg -i ../*.deb

    修复可能的依赖问题
    apt install -f
```


## ref

    [BuildingTutorial]("https://wiki.debian.org/BuildingTutorial")
