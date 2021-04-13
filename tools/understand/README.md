# Linux下安装和使用

## ubuntu
```
# 解压
> tar xzvf Understand-5.1.1029-Linux-64bit.tgz

> cd scitools/bin/linux64
> ./understand

输入注册码即可使用
```

## fedora
```
错误信息
./understand: symbol lookup error: /lib64/libfontconfig.so.1: undefined symbol: FT_Done_MM_Var
调整：
> cd scitools/bin/linux64
> sudo mv libfreetype.so.6 libfreetype.so.6.bak
```
