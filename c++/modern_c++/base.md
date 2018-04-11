# 一些基本东西的记录

## 实现或者删除copy/move constructor/operators
```
class MyClass;

MyClass(const MyClass &) = delete;
MyClass(MyClass &&) = delete;
MyClass &operator = (const MyClass &) = delete;
MyClass &operator = (MyClass &&) = delete;
```

## ref
    [SimpleList-A C# to C++ comparison](https://www.codeproject.com/Articles/1236991/SimpleList-A-Csharp-to-Cplusplus-Comparison)
