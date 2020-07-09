# 一些转key的记录

## JKS格式转PEM（PEM用于不同类型的X.509v3文件）
```
可能java开发直接给你的是xxx.keystore文件
```
### 检查keystore内容
```
> keytool -list -keystore prod_encrypt.keystore
```

### 转为pkcs12格式
```
> keytool -importkeystore -srckeystore prod_encrypt.keystore -destkeystore prod_encrypt.p12 -deststoretype PKCS12
```

### 转为pem
```
> openssl pkcs12 -in prod_encrypt.p12 -out prod_encrypt.pem
```

### 去掉pem密码
```
> openssl rsa -in encryedprivate.key -out unencryptd.key
```

## PFX转PEM
```
> openssl pkcs12 -in jcbank_pri.pfx -nodes -out jcbank_pri.pem
如果有密码，抹掉密码
> openssl rsa -in jcbank_pri.pem -out jcbank_pri.pem
```

## CER转PEM
```
> openssl x509 -inform der -in businessgate.cer -out businessgate.pem
```

## REF
    [CONVERT PRIVATE SSL KEY FROM JKS TO PEM FORMAT](https://cinhtau.net/2016/08/09/convert-private-ssl-key-from-jks-to-pem-format/)
