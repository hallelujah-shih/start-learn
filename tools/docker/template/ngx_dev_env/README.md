# nginx模块测试环境
```
```

## 基本使用
```
docker-compose run ngx_dbg bash

# set coredump (man core) %s sig
echo "/tmp/core.%e.%s.%p.%t" > /proc/sys/kernel/core_pattern

// sysctl -w kernel.core_pattern="%e-%s.core"
```