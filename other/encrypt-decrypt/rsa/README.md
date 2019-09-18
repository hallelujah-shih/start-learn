# RSA使用demo

## 创建钥匙对
```
> openssl genrsa -out private_key.pem 1024
> openssl rsa -in private_key.pem -pubout -out public_key.pem
```
