# Chrome

## Fedora换个WIFI环境后Chrome无法打开
```
journalctl --since="2024-09-16" -g chrome --no-pager
错误信息如下：
Sep 16 14:05:50 fedora google-chrome.desktop[4698]: [4691:4691:0916/140550.273000:ERROR:process_singleton_posix.cc(353)] The profile appears to be in use by another Google Chrome process (4725) on another computer (sc.10086.cn).  Chrome has locked the profile so that it doesn't get corrupted.  If you are sure no other processes are using this profile, you can unlock the profile and relaunch Chrome.
Sep 16 14:05:50 fedora google-chrome.desktop[4698]: [4691:4691:0916/140550.288171:ERROR:message_box_dialog.cc(144)] Unable to show a dialog outside the UI thread message loop: Google Chrome - The profile appears to be in use by another Google Chrome process (4725) on another computer (sc.10086.cn).  Chrome has locked the profile so that it doesn't get corrupted.  If you are sure no other processes are using this profile, you can unlock the profile and relaunch Chrome.

解决方法：
1. cd $HOME/.config/google-chrome
2. rm Singleton* -rf

重新打开即可
```