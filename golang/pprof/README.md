# pprof基本使用
```
代码中引入
_ "net/http/pprof"
```

## 监听http
```
go func() {
	log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

## 监听uds
```
unixAddr := "/tmp/pprof-test.sock"
fileInfo, err := os.Stat(unixAddr)
if err == nil {
	if stat, ok := fileInfo.Sys().(*syscall.Stat_t); ok {
		linkCount := stat.Nlink
		if linkCount <= 1 {
			os.Remove(unixAddr)
		}
	}
}
unixListener, err := net.Listen("unix", unixAddr)
if err != nil {
	log.Fatal("Error creating Unix socket:", err)
}
defer os.Remove(unixAddr) // 大概率清理不掉
// 启动 HTTP 服务
go func() {
	log.Fatal(http.Serve(unixListener, nil))
}()
```

### uds转http
```
socat TCP-LISTEN:1337,bind=127.0.0.1,reuseaddr,fork UNIX-CONNECT:/tmp/pprof-test.sock
或
curl --unix-socket /tmp/pprof-test.sock -X GET http://localhost/debug/pprof/profile?seconds=30 -o profile.out
```

## 性能分析
```
基本使用方法：
如果是远程服务器，可以先做个端口转发：
	ssh -L 8088:127.0.0.1:1303 root@remote-host-name

1. 本地文件
	go tool pprof -http=127.0.0.1:8000 profile.out
2. http
	go tool pprof -http="127.0.0.1:8000" "http://localhost:1337/debug/pprof/profile?seconds=30"
```

### CPU
```
go tool pprof -http="127.0.0.1:8000" http://localhost:8088/debug/pprof/profile?seconds=30
```

### 内存
```
inuse_space: See memory size in use at time of profiling that hasn't been released.
inuse_objects: See object count in use at time of profiling and that hasn't been released.
alloc_space: See allocated memory size across the lifetime of the application.
alloc_objects: See allocated object count across the lifetime of the application.

go tool pprof -alloc_objects -svg http://localhost:8088/debug/pprof/heap > alloc_objects.svg
go tool pprof -alloc_space -cum -svg http://localhost:8088/debug/pprof/heap > alloc_space.svg
go tool pprof -inuse_space -cum -svg http://localhost:8088/debug/pprof/heap > inuse_space.svg
go tool pprof -http="127.0.0.1:8000" http://localhost:8088/debug/pprof/heap
```

### block
```
如果基于net/http/pprof，应用程序需要调用runtime.SetBlockProfileRate来配置采样频率。
// 1 代表 全部采样，0 代表不进行采用， 大于1则是设置纳秒的采样率
runtime.SetBlockProfileRate(1)
curl http://localhost:1337/debug/pprof/block?seconds=60 -o block.out
go tool pprof -http="127.0.0.1:8000" block.out
```

### mutex
```
如果基于net/http/pprof，应用程序需要调用runtime.SetMutexProfileFraction来配置采样频率。
// 0 代表不进行采用， 1则全部采用，大于1则是一个随机采用
runtime.SetMutexProfileFraction(1)
```

## ref
   * [Analyzing and improving memory usage in Go](https://medium.com/safetycultureengineering/analyzing-and-improving-memory-usage-in-go-46be8c3be0a8)
