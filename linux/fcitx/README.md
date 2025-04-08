# Fcitx安装使用
```
ibus默认的pinyin输入法一言难尽，某日和IDE一起工作一直出问题，遂改fcitx
```

## fedora 39 + gnome
```
1. install
    # 安装fcitx5
    $ sudo dnf install fcitx5 fcitx5-gtk fcitx5-qt fcitx5-configtool fcitx5-lua fcitx5-chinese-addons fcitx5-table-extra fcitx5-rime
    # 安装gnome插件https://extensions.gnome.org/extension/261/kimpanel/

2. set env(此处我设置在profile中的)
    export LC_CTYPE=zh_CN.UTF-8
    export XMODIFIERS="@im=fcitx"
    export QT_IM_MODULE=fcitx

3. 恩，不是很懂得，反正设置了
    gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gtk/IMModule':<'fcitx'>}"

4. 做个autostart(cat $HOME/.config/autostart/fcitx-autostart.desktop)
    [Desktop Entry]
    Name=Fcitx
    GenericName=Input Method
    Comment=Start Input Method
    Exec=fcitx5 -d -r
    Icon=fcitx
    Terminal=false
    Type=Application
    Categories=System;Utility;
    StartupNotify=false
    NoDisplay=true

4. reboot

5. 可以简单诊断下看缺啥
    fcitx5-diagnose

6. 配置输入法(libpinyin)
    $ fcitx5-configtool
    把 trigger input method 改为 Lctrl Lshift
    Prev Page 改为 pgup
    Next Page 改为 pgdn

7. 按下 shift 就是拼音了
```

## ubuntu 18.04 + gnome
```
```

## ref
* [fcitx5 install](https://fcitx-im.org/wiki/Install_Fcitx_5)
* [fcitx5 config](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland)