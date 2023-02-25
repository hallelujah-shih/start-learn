# lua nginx module指令顺序
    [指令相关资料](https://github.com/openresty/lua-nginx-module#directives)

## 指令顺序概览
```
重要阶段的一些重要指令
```

### 初始化阶段(initialization phase)
```
init_by_lua* -> init_worker_by_lua*
```

### 重写/访问阶段(Rewrite/Access phase)
```
[ssl_certificate_by_lua*] -> set_by_lua* -> rewrite_by_lua* -> access_by_lua*
```

### 内容处理阶段(content phase)
```
[content_by_lua*] -> header_filter_by_lua* -> body_filter_by_lua*
[balancer_by_lua*]->
```

### 日志阶段(log phase)
```
log_by_lua*
```

## lua的nginx API
### 请求相关操作
```
请求头相关操作
ngx.resp.get_headers(max_headers?, raw?)
ngx.req.get_headers(max_headers?, raw?)
ngx.req.set_headers(header_name, header_value) header_value可以是数组
ngx.req.raw_header(no_request_line?)
ngx.req.clear_header(header_name) 清理指定名字的请求头信息
ngx.send_headers() 显式发送响应头

判断是否是内部请求
ngx.req.is_internal()

获取创建连接的时间
ngx.req.start_time() 返回浮点数，单位毫秒ngx_http_log_module的$request_time的纯lua为ngx.now() - ngx.req.start_time()

获取请求的HTTP协议版本
ngx.req.http_version()

获取方法
ngx.req.get_method()
ngx.req.set_method()

获取uri信息
ngx.req.set_uri(uri, jump?)

获取参数信息
ngx.req.set_uri_args(args) 字符串或字典
ngx.req.get_uri_args(max_args?)
ngx.req.get_post_args(max_args?) 获取post查询的参数(mime类型为application/x-www-form-urlencoded),需要先调用ngx.req.read_body
ngx.encode_args(table)
ngx.decode_args(str, max_args?)

数据体相关操作
ngx.req.read_body()同步读取请求的数据体，不会阻塞nginx的event loop
ngx.req.discard_body() 明确的丢弃请求数据体
ngx.req.get_body_data() 性能高于ngx.var.request_body和ngx.var.echo_request_body
ngx.req.get_body_file() 如果数据存储在磁盘上用这个函数
ngx.req.set_body_data(data) 设置当前请求的请求体(如果请求体未被读取，此操作将会被忽略)
ngx.req.set_body_file(file_name, auto_clean?)
ngx.req.init_body(buffer_size?) 为当前请求创建一个空白的请求体并初始化，为后续ngx.req.append_body和ngx.req.finish_body使用
ngx.req.append_body(data_chunk) 向ngx.req.init_body创建的空白请求体中写入数据，当在内存中不能保存数据时，将会写入到临时文件中保存
ngx.req.finish_body()
```

### 时间相关操作
```
ngx.sleep(seconds)
ngx.today() "yyyy-mm-dd"
ngx.time() 返回单位为秒，此时间带有缓存
ngx.now() 返回单位为秒，此时间带有缓存，精确到毫秒的浮点数
ngx.update_time() 更新nginx当前时间的缓存
ngx.localtime() 返回当前时间的时间戳"yyyy-mm-dd hh:mm:ss",时间取自时间缓存，非系统调用
ngx.utctime() 和ngx.localtime()类似
ngx.cookie_time(sec) 直接输出的是cooke的过期时间格式
ngx.http_time(sec) 用于返回http header的时间，如Last-Modified所用时间
ngx.parse_http_time(str) 用于分析http header中的时间
ngx.timer.at(delay, callback, user_arg1, user_arg2, ...) 定时器

```

### 打印/输出相关操作
```
ngx.print(...)
ngx.say(...) 和ngx.print类似但是ngx.say会发送换行
ngx.log(log_level, ...)
ngx.flush(wait?)
```
### 字符串操作
```
ngx.re.match(subject, regex, options?, ctx?, res_table?)
ngx.re.find(subject, regex, options?, ctx?, nth?) 和match类似，但是只返回匹配到字符串的beginning index和end index
ngx.re.gmatch(subject, regex, options?) 和match类似，但是返回的是iter
ngx.re.sub(subject, regex, replace, options?) 
ngx.re.gsub(subject, regex, replace, options?) 和re.sub类似但是是全局替换
```

### 数据结构存储相关操作
```
ngx.shared.DICT
    get
    get_stale
    set
    safe_set
    add
    safe_add
    replace
    delete
    incr
    lpush
    rpush
    lpop
    rpop
    llen
    flush_all
    flush_expired
    get_keys
```

### socket相关操作
```
ngx.req.socket 获取裸的socket，用于直接操作流数据
ngx.socket.udp() 创建udp套接字
    setpeername(host, port) | setpeername("unix:/path/unix-domain.socket")
    send(data)
    receive(size?)
    close()
    settimeouttime(time)  like s (second), ms (millisecond), m (minute)
ngx.socket.tcp
    connect(host, port, options_table?) | connect("unix:/path/unix-domain.socket")
    sslhandshake(reused_session?, server_name?, ssl_verify?, send_status_req?)
    send(data)
    receive(size?) | receive(pattern?)
    close()
    settimeout(time)
    setoption(option, value?)
    receiveuntil(pattern, options?)
    setkeepalive(timeout?, size?)
    getreusedtimes()
ngx.socket.stream 是ngx.socket.tcp的别名
ngx.socket.connect(host, port) | ngx.socket.connect("unix:/path/unix-domain.socket") 是sock = ngx.socket.tcp()  sock:connect(...)的简化形式
```

### balancer相关
```
[详细描述地址](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/balancer.md)
[经典讨论](https://groups.google.com/forum/#!topic/openresty-en/6b9HgG_0xas)
balancer.set_current_peer(host, port) 设置当前查询的后端的IP地址和端口（host需要在access_by_lua*等阶段将域名解析出来）
balancer.set_more_tries(count) 
balancer.get_last_failure() 获取失败细节
balancer.set_timeouts(connect_timeout, send_timeout, read_timeout)
```

### thread相关
```
ngx.thread.spawn
ngx.thread.wait
ngx.thread.kill
ngx.on_abort
```
