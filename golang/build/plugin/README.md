# buildmode plugin

## 示例使用
```
go build -o plugin main.go

cd plugins/p1
go build -buildmode=plugin

cd ../..
./plugin -p plugins/p1/p1.so
```

## ref
- [go-plugindemo](https://github.com/jvmatl/go-plugindemo)