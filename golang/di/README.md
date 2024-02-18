# 依赖注入简单使用
```
原始项目在my-proj下面
可以直接用 go run main.go输出hello world

wire-go-v1采用wire进行依赖注入改造
专注于对象以及对象本身的关系，而构建对象本身以及之间的初始化关系交由工具自动生成
wire gen
go build
./my-proj 可以达到同样的目的
```