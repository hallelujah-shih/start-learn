# kernel dev env
```
vscode内核开发配置
```

## 下载源码

```
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.41.tar.xz
unxz linux-5.10.41.tar.xz
tar xf linux-5.10.41.tar
```

## vscode配置
```
cd linux-5.10.41
git clone git@github.com:amezin/vscode-linux-kernel.git .vscode

# 常规build
make defconfig
make -j 8
python .vscode/generate_compdb.py

# Out-of-tree builds
make O=../linux-build defconfig
make -j 8 O=../linux-build
python .vscode/generate_compdb.py -O ../linux-build
```
