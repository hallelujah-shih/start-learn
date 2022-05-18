# cfssl使用示例

## 安装
```
go get -u github.com/cloudflare/cfssl/cmd/cfssl
go get -u github.com/cloudflare/cfssl/cmd/cfssljson
```

## 创建一个根CA
```
cfssl gencert -initca root.json | cfssljson -bare root
```

## 创建一个中间CA
```
创建一个中间CA
cfssl gencert -initca intermediate.json | cfssljson -bare intermediate
// 根据已有的key生成csr
// cfssl gencsr -key intermediate-key.pem intermediate.json |cfssljson -bare intermediate
签发一个中间CA
cfssl sign -ca root.pem -ca-key root-key.pem -config cfssl.json -profile intermediate_ca intermediate.csr | cfssljson -bare intermediate
```

## 签发一个服务端证书
```
cfssl gencert -ca intermediate.pem -ca-key intermediate-key.pem -config cfssl.json -profile=server host.json | cfssljson -bare 200-server
```

## 签发一个客户端证书
```
cfssl gencert -ca intermediate.pem -ca-key intermediate-key.pem -config cfssl.json -profile=client host.json | cfssljson -bare client-1
```

## 签发一个peer证书
```
cfssl gencert -ca intermediate.pem -ca-key intermediate-key.pem -config cfssl.json -profile=peer host.json | cfssljson -bare node-peer
```

## ref
* [How to use cfssl to create self signed certificates](https://rob-blackbourn.medium.com/how-to-use-cfssl-to-create-self-signed-certificates-d55f76ba5781)
* [客户端证书验证在不同组件中的实现逻辑](https://l81gi68o32.larksuite.com/docs/docuswuH3j9uDmOP35tYOyDUlnh)