# wireshark

## Linux下设置
```
1. setcap设置（可能是/usr/sbin/dumpcap）权限
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap

2. 只针对wireshark组有效
    sudo groupadd -s wireshark
    sudo gpasswd -a $USER wireshark
    sudo chgrp wireshark /usr/bin/dumpcap
```
