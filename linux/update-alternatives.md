# update-alternatives
```
一些简易脚本
```

## clang
```
安装特定版本的clang
sudo apt install clang-10 clang-format-10 llvm-dev-10

设置为默认值
sudo update-alternatives --remove-all clang
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-10 100
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-10 100
sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-10 100
sudo update-alternatives --install /usr/bin/llc llc /usr/bin/llc-10 100
```
