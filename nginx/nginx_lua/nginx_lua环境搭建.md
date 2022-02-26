# 环境搭建
```
此处测试环境的搭建使用了openresty
```

## 编译openresty
```
> tar xzvf openresty-1.x.x.x.tar.gz
> cd openresty
> ./configure --prefix=/opt/nginx --group=nginx --user=nginx --conf-path=/etc/nginx/nginx.conf --pid-path=/run/nginx.pid --sbin-path=/usr/sbin/nginx --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-debug
> make -j 4 && make install
创建nginx分组和用户
> groupadd -f nginx
> useradd -g nginx nginx
改变记录日志的目录权限
> chown -R nginx:nginx /var/log/nginx
启动nginx
> nginx
看是否正常监听
> netstat -tpnl
```
