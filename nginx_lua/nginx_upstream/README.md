# 测试使用方式
```
> sudo docker-compose up
> curl "http://localhost:5555/"
> cat log/error.log
```

## debug nginx 
```
ps aux|grep nginx
找出work process

cd /usr/src/openresty-xxxx
gdb -p pid

* 用tmux分割窗口来操作，不然没法请求
```
