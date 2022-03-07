# Linux内核开发环境准备

## 依赖安装

## 单独内核头文件目录（为了稳定，便于编辑器配置）
```
sudo dnf -y install flex bison
此处假设以内核5.8.12为例

cp linux-5.8.12.tar.xz /usr/src/kernels/
cd /usr/src/kernels/
unxz linux-5.8.12.tar.xz
tar xvf linux-5.8.12.tar

# make tinyconfig
make oldconfig

在Makefile中加入
show-includes:
	@$(foreach include, $(LINUXINCLUDE), echo $(include);)
	@$(foreach include, $(USERINCLUDE), echo $(include);)

并执行：
make show-includes | sort -u
可能得到如下输出：
-I./arch/x86/include
-I./arch/x86/include/generated
-I./arch/x86/include/generated/uapi
-I./arch/x86/include/uapi
-I./include
-I./include/generated/uapi
-I./include/uapi
-include
./include/linux/kconfig.h
```

## vscode看内核代码
```
1. 安装global （apt install global）
2. vscode 安装C/C++ GNU Global
    其中在项目的settings.json里面指定global相关路径
    "gnuGlobal.globalExecutable": "/usr/bin/global",
    "gnuGlobal.gtagsExecutable": "/usr/bin/gtags",
    // 指明生成的符号表存放在哪个位置
    "gnuGlobal.objDirPrefix": "/mnt/.global"
3. ctrl + shift + p 执行 global: rebuild gtags database
```

## ref
    [ycm cfg kernerl develop](https://ops.tips/blog/developing-ebpf-with-autocompletion-support/)
    [VSCode 阅读 Linux 代码怎么才不卡顿？这样做才能快的飞起！](https://mp.weixin.qq.com/s/dK5P4nbGw7IvzULDTLVYSg)
