# XDP

## 基本环境
```
个人所用内核版本为4.20.10，以下包括config等说明均以此
```

### 开发环境
```
Fedora
$ sudo dnf install -y git gcc ncurses-devel elfutils-libelf-devel bc openssl-devel libcap-devel clang llvm graphviz

Ubuntu
$ sudo apt-get install -y make gcc libssl-dev bc libelf-dev libcap-dev clang gcc-multilib llvm libncurses5-dev git pkg-config libmnl bison flex graphviz
```

### 内核编译选项
```
CONFIG_CGROUP_BPF=y
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
CONFIG_NET_SCH_INGRESS=m
CONFIG_NET_CLS_BPF=m
CONFIG_NET_CLS_ACT=y
CONFIG_BPF_JIT=y
CONFIG_LWTUNNEL_BPF=y
CONFIG_HAVE_EBPF_JIT=y
CONFIG_BPF_EVENTS=y
# 这个可有可无
CONFIG_TEST_BPF=m
```

### 内核配置
```
1. 加载bpf fs
    a. 命令行
        $ mount bpffs /sys/fs/bpf -t bpf
    b. /etc/fstab
        bpffs /sys/fs/bpf bpf defaults 0 0
    c. 写成服务
2. 开启bpf jit(如果perf top发现__bpf_prog_run()高，可以开启，也可以一步到位)
    $ sysctl net/core/bpf_jit_enable=1 
```

## REF
    [Troubleshooting BPF]("https://prototype-kernel.readthedocs.io/en/latest/bpf/troubleshooting.html")
    [cilium]("https://cilium.io/")
    [katran]("https://github.com/facebookincubator/katran")
    [gcc]("https://gcc.gnu.org/onlinedocs/gcc-8.3.0/gcc/")
    [asm goto not supported]("https://lore.kernel.org/patchwork/patch/903103/")
