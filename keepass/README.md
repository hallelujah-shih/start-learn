# keepass 使用
## keepass在Fedora 28～上增加plugin
```
> sudo mkdir -p /usr/lib/keepass/plugins
> sudo cp *.plgx /usr/lib/keepass/plugins
```

## 解决方块字
```
sudo vim /usr/bin/keepass
并加入一行
export LANG=zh_CN.utf8
```
