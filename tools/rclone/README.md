# rclone基本使用
```
记录软件的使用情况
```

## OneDrive
```
记录OneDrive在Fedora 29下的配置和使用情况
> curl https://rclone.org/install.sh | sudo bash

剩下详情参见: https://rclone.org/onedrive/

主动挂到本地目录脚本如下：
#!/bin/bash

mkdir -p ${HOME}/onedrive
rclone mount remote:/ ${HOME}/onedrive/ --daemon

```

## REF
    [onedrive rclone](https://rclone.org/onedrive/)
