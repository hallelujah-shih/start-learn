# 测试共享库

## 没作用版本v1
```
make v1
./a.out

make clean
```

## 有作用版本v2
```
make v2
./a.out

make clean

v2中注释掉main中stack_buf_overflow_func的调用来测试内存泄露
```