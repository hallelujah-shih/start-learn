# golang 编译其他语言能使用的动态链接库

## 将golang的函数导出为C函数符号
```
1. 增加注释 //export FuncName
2. 该函数所在go文件必须有import "C"
3. 该功能必须属于main package
4. 函数签名不得包含struct、interface、array、可变参数
```

## ref
- [using-dynamic-or-shared](https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dynamic_or_shared.html)
- [buidl-and-use-go-packages-as-c-libraries](https://medium.com/swlh/build-and-use-go-packages-as-c-libraries-889eb0c19838)
- [go-cshared-examples](https://github.com/vladimirvivien/go-cshared-examples)
