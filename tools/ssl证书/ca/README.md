# 证书更换方案

## 证书生成方案
```
// ca目录下执行

// 1. 创建CA
cfssl gencert -initca root.json | cfssljson -bare root

// 2. 签发一个节点证书(此处可以由中间证书签发，效果一样)
cfssl gencert -ca root.pem -ca-key root-key.pem -config cfssl.json -profile=peer host.json | cfssljson -bare node-peer

// 3. 合并证书
cat node-peer.pem node-peer-key.pem root.pem > turbo.pem
```

## 测试
```
将ca目录下的turbo.pem分别复制到nginx/server/ssl和nginx/upstream/ssl目录下

cd nginx
docker-compose up

docker-compose exec server curl localhost
```

## QA

### 为什么不直接用自签名的根证书
```
更换困难，不能做到无感更换
```

### 为什么要用签发的证书
```
因为签发的证书可以更换，可以出现同时新老证书同在的情况
```

### jsl-waf是否需要更改
```
SAN中若有turbo，那么线上将不用更改
```

## ref
* [x509v3 config](https://www.openssl.org/docs/man1.0.2/man5/x509v3_config.html)