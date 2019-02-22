# XDP hello
```
第一个xdp测试程序
```

## 基本使用
```
> make
> sudo mount -t bpf bpffs /sys/fs/bpf/
> sudo ip -force link set dev ens32 xdp object xdp_dummy.o verbose
> curl www.baidu.com # 已经不能访问了
> sudo ip link set dev ens32 xdp off
> curl www.baidu.com # success
```
