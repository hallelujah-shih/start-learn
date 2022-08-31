# 一些转key的记录

## Creating PKCS12 Keystores
```
openssl pkcs12 -export -out prototype-client.p12 \
  -inkey prototype-client-key.pem -in prototype-client.pem -certfile ca.pem
openssl pkcs12 -export -out prototype-server.p12 \
  -inkey prototype-server-key.pem -in prototype-server.pem -certfile ca.pem
```

## Creating JKS Keystore and Truststore
```
Creating the jks from the p12:
keytool -importkeystore -srckeystore prototype-client.p12 \
  -storetype pkcs12 -destkeystore prototype-client.jks \
  -deststoretype jks

keytool -importkeystore -srckeystore prototype-server.p12 \
  -storetype pkcs12 -destkeystore prototype-server.jks \
  -deststoretype jks

Creating a truststore：
keytool -import -file ca.pem -alias 'PrototypeCA' -keystore truststore.jks
```

## Creating a PKCS8 Keystore
```
This will generate an encrypted pkcs8 keystore, use -nocrypt if you don't want that:

openssl pkcs8 -topk8 -in prototype-server-key.pem -out prototype-server-key.p8
```

## 加解密私钥
```
加：
openssl rsa -aes256 -in prototype-server-key.pem -out prototype-server-key-enc.pem

解：
openssl rsa -in prototype-server-key-enc.pem -out prototype-server-key.pem
```

### Creating SSH Keypairs from PKCS12 Keystores
```
ssh-keygen -f prototype-client-key.pem -y > prototype-client.pub
```

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
    [Sample Cloudflare SSL (CFSSL) Certificate Authority](https://github.com/drewfarris/sample-cfssl-ca)
