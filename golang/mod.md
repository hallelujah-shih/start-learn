# go mod
```
go mod的一些使用说明
```

## GoProxy设置
```
国内设置：
    export GOPROXY=https://goproxy.io

    # 阿里云支持
    export GOPROXY=https://mirrors.aliyun.com/goproxy

    # 七牛云支持
    export GOPROXY=https://goproxy.cn
```

## 内网gitlab支持
```
设置access-token（settings->access tokens->personal access token）

> git config --global http.extraheader "PRIVATE-TOKEN: my-access-token"

将 git请求从ssh转为http
> git config --global url."git@git.xwfintech.com".insteadOf "http://git.xwfintech.com"
```
