# 测试1
```
宿主机为Fedora 39，gcc版本较高，即不再在makefile中指定版本方式编译
sudo dnf -y install libasan libasan-static libstdc++-static
```

## 编译
    make using-gcc
    make using-gcc-static
    make using-clang

## ref
    [Compiling with Address Sanitizer (ASAN) with CLANG and with GCC-4.8](https://gist.github.com/kwk/4171e37f4bcdf7705329)
