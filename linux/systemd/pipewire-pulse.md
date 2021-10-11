# pipewire-pulse
```
Fedora 34上服务报错

Sep 16 10:04:00 fedora pipewire-pulse[2154]: mempool 0x555dcdf5d790: Failed to create memfd: Too many open files
Sep 16 10:04:00 fedora pipewire-pulse[2154]: stream 0x555de11e1b50: can't make node: Too many open files

直接导致了系统音频跪了，不管是虚拟机还是宿主机均无声音

且直接导致了vmware上的虚拟机（有音频输出的）极为卡顿，qemu上的win 10不管是否是virt-viewer连接，均可能无响应，点击wait无用，点击force quit后再次进入是一样的情况，当删除qemu的设备中的sound card后，虽然宿主机一致继续报错，但是虚拟机再无卡顿，kill掉 pipewire-pulse进程后会重新拉起此进程，此时音频又恢复了，证明就是音频管理的问题。
```

## systemd增加ulimit选项
```
/lib/systemd/user/pipewire-pulse.service
在ExecStart前增加变量
LimitNOFILE=65536
```


## systemd的ulimit选项映射关系
```
Directive        ulimit equivalent     Unit
LimitCPU=        ulimit -t             Seconds
LimitFSIZE=      ulimit -f             Bytes
LimitDATA=       ulimit -d             Bytes
LimitSTACK=      ulimit -s             Bytes
LimitCORE=       ulimit -c             Bytes
LimitRSS=        ulimit -m             Bytes
LimitNOFILE=     ulimit -n             Number of File Descriptors
LimitAS=         ulimit -v             Bytes
LimitNPROC=      ulimit -u             Number of Processes
LimitMEMLOCK=    ulimit -l             Bytes
LimitLOCKS=      ulimit -x             Number of Locks
LimitSIGPENDING= ulimit -i             Number of Queued Signals
LimitMSGQUEUE=   ulimit -q             Bytes
LimitNICE=       ulimit -e             Nice Level
LimitRTPRIO=     ulimit -r             Realtime Priority
LimitRTTIME=     No equivalent


If a ulimit is set to 'unlimited' set it to 'infinity' in the systemd config

ulimit -c unlimited is the same as LimitCORE=infinity
ulimit -v unlimited is the same as LimitAS=infinity
ulimit -m unlimited is the same as LimitRSS=infinity
```

## ref
[how-to-set-ulimits-on-service-with-systemd](https://unix.stackexchange.com/questions/345595/how-to-set-ulimits-on-service-with-systemd)
