# Fcitx安装使用
```
ibus默认的pinyin输入法一言难尽，某日和IDE一起工作一直出问题，遂改fcitx
```

## fedora 39 + gnome
```
1. install
    sudo dnf -y install fcitx fcitx-configtool fcitx-data fcitx-libpinyin fcitx-table-chinese

2. set env(此处我设置在profile中的)
    export LC_CTYPE=zh_CN.UTF-8
    export XMODIFIERS="@im=fcitx"
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx

3. 恩，不是很懂得，反正设置了
    gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gtk/IMModule':<'fcitx'>}"

4. 做个autostart(cat $HOME/.config/autostart/fcitx-autostart.desktop)
    [Desktop Entry]
    Name=Fcitx
    GenericName=Input Method
    Comment=Start Input Method
    Exec=fcitx -d -r
    Icon=fcitx
    Terminal=false
    Type=Application
    Categories=System;Utility;
    StartupNotify=false
    NoDisplay=true

4. reboot

5. 可以简单诊断下看缺啥
    fcitx-diagnose

6. 配置输入法(libpinyin)
    fcitx-config-gtk3
    把 trigger input method 改为 Lctrl Lshift
    extra key for trigger 改为 disable
    Prev Page 改为 pgup
    Next Page 改为 pgdn

7. 按下 shift 就是拼音了
```

## ubuntu 18.04 + gnome
```
```

## ref
* [Inputting Japanese text in Linux and some BSDs](https://srobb.net/jpninpt.html#Fedora)
* [fcitx](https://wiki.archlinux.org/title/fcitx)
* 