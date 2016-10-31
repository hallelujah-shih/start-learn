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

test_ser.py是为了测试实现的一个upstream服务器(为了产生rst数据包的报文)
```

## 注意
```
在使用balancer的时候一定要注意控制peer的信息，特别是set_more_tries不设置的时候nginx中u->peer.tries == 0，但是单set_current_peer时，得到的是未关闭的socket连接时(keep-alive)，产生错误之后依然会重入balancer。


示例代码：
s = requests.Session()
s.get("http://localhost")
s.get("http://localhost")
s.get("http://localhost")

s.get("http://localhost") 注意加断点看
```
