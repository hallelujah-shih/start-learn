# pprof基本使用

## 构建tunnel，转发到远程机器端口
```
ssh -L 8088:127.0.0.1:1303 root@remote-host-name
```

## 分析内存
```
inuse_space: See memory size in use at time of profiling that hasn't been released.
inuse_objects: See object count in use at time of profiling and that hasn't been released.
alloc_space: See allocated memory size across the lifetime of the application.
alloc_objects: See allocated object count across the lifetime of the application.

go tool pprof -alloc_objects -svg http://localhost:8088/debug/pprof/heap > alloc_objects.svg
go tool pprof -alloc_space -cum -svg http://localhost:8088/debug/pprof/heap > alloc_space.svg
go tool pprof -inuse_space -cum -svg http://localhost:8088/debug/pprof/heap > inuse_space.svg

go tool pprof -http="127.0.0.1:8000" http://localhost:8088/debug/pprof/heap

# or offline
go tool pprof -http=127.0.0.1:8000 profile_name-heap.pb.gz
```

## ref
* [Analyzing and improving memory usage in Go](https://medium.com/safetycultureengineering/analyzing-and-improving-memory-usage-in-go-46be8c3be0a8)