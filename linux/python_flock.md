# Python文件锁说明
```
在写dpvs的管理程序的时候，使用了fcntl.flock
每次我kill掉dpvs进程的时候，重新启动都会失败，提示锁不上。
```

## 原因分析
```
可以通过检查/proc/locks中的锁信息，以及lsof pidfile来看，发现pidfile还在被继续持有，而持有它的当然不是已经被kill掉的进程，而是子进程。
fcntl.flock是可能伴随fd一起被子进程继承的
```

## 解决办法
```
fcntl.flock替换为fcntl.lockf或subprocess.Popen创建子进程的时候，带上参数close_fds=True
```

## 总结
```
1. fcntl() locks are the most reliable
2. Most often, lockf() is implemented as "shorthand" for fcntl()
3. fcntl() and flock() have different semantics wrt. inheritance and automatic releases
    fcntl/lockf不会被子进程继承，而flock我恰好躺枪，使用了subprocess.Popen，且没有关闭句柄
```
