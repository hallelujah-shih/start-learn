# 输入法问题
```
此处环境为Fedora 36，Ubuntu类似
输入法为ibus pinyin
现象：输入中文存在各种问题
```

## 修改vm options
```
打开 help -> edit custom vm options
加入一行：-Drecreate.x11.input.method=true
重启ide
```
