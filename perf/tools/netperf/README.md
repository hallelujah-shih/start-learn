# NETPERF
```
netperf的编译使用
```

## install
```
> git clone https://github.com/HewlettPackard/netperf.git
> cd netperf
> autoreconf -ivf
# 若出现error: possibly undefined macro: AC_CHECK_SA_LEN 。。。。
# 编辑configure.ac并注释掉AC_CHECK_SA_LEN(ac_cv_sockaddr_has_sa_len)
# 并重新执行autoreconf -ivf
> ./configure
> make && make install
# 若编译错误找不到makeinfo，需要安装texinfo
```
