# 杂项

## 编译选项

### ASan
```
# ASan
export CC="clang -fsanitize=address"
export CXX="clang++ -fsanitize=address -fno-sanitize=vptr"

# UBSan
export CC="clang -fsanitize=undefined"
export CXX="clang++ -fsanitize=undefined -fno-sanitize=vptr"
```