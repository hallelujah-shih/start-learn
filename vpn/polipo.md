# polipo
```
为了大家都能够通过http proxy访问外网，而polipo能够桥接shadowsocks，这样避免了某些设备需要付费买软件的尴尬
```

## polipo 安装
```
> git clone https://github.com/jech/polipo.git
> cd polipo && make
> cp polipo /usr/bin/ 
> cp config.sample /etc/polipo.conf
```

## 简单测试
```
> polipo socksParentProxy=localhost:1080
> curl --proxy http://127.0.0.1:8123 https://www.google.com
```

## 配置设置
```
vim /etc/polipo.conf

socksParentProxy = “127.0.0.1:1080″
socksProxyType = socks5
proxyAddress = "0.0.0.0"
proxyPort = 8123
```

## 运行
```
> polipo -c /etc/polipo.conf
```

## 测试
```
参照简单测试即可，然后某果就可以不用买ss了
```

## reference
[polipo](https://www.irif.univ-paris-diderot.fr/~jch//software/polipo/)
[polipo git](https://github.com/jech/polipo.git)
[polipo install](http://www.codevoila.com/post/16/convert-socks-proxy-to-http-proxy-using-polipo)
