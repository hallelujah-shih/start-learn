# Linux内核相关头文件和宏配置

## 宏和include目录
```
# 宏目录
include/linux/kconfig.h
include/generated/autoconf.h
include/linux/autoconf.h (old kernel)

# include目录
include
include/uapi
include/generated
include/generated/uapi
arch/architecture/include
arch/architecture/include/uapi
arch/architecture/include/generated
arch/architecture/include/generated/uapi
```

## 符号
```
__KERNEL__
__GNUC__
```

## GCC
```
/lib/gcc/<arch>/<version>/include
```

### 编译选项
``
-nostdinc
-iwithprefix
```
