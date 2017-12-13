# Dep使用
```
dep工具是golang的依赖管理工具
简单介绍其使用
```

## 安装
```bash
$ go get -u -v github.com/golang/dep/cmd/dep
```

## 使用
```bash
# 初始化
$ dep init
# 增加依赖
$ dep ensure -add github.com/foo/bar
# 查看状态
$ dep status
# 更新
$ dep ensure -update github.com/some/project
# 删除
# 1. 从代码的import中删除
# 2. 从Gopkg.toml中[[constraint]]中删除
# 3. 执行下面命令 
$ dep ensure
```
