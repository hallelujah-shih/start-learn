# source code pro字体安装

## ubuntu 20.04
```
在release页面下载：https://github.com/adobe-fonts/source-code-pro/releases
选择OTF即可，假设文件名为： source-code-pro.zip

解压：
unzip -d /usr/share/fonts/opentype/scp source-code-pro.zip
or:
unzip -d $HOME/.fonts/scp source-code-pro.zip

更新：
fc-cache -f -v
 
```
