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

## 插件推荐

### keepasshelper
```
已经缺乏维护了，特别是在Linux上，plugin容易不生效（能看见，但是不能补全）
```

### keepassnatmsg
```
下载：
    https://github.com/smorks/keepassnatmsg
将KeePassNatMsg-kp2.45.plgx移到插件存放位置，重启keepass
安装KeePassXC-Browser插件

* 我fedora上没法补全，没法使用，需要检查 $HOME/.keepassnatmsg目录下是否有keepassnatmsg-proxy.exe
* 若没有，手动下载，并放入即可，下载地址：https://github.com/smorks/keepassnatmsg-proxy/releases/

```
