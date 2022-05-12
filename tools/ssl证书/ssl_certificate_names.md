# SSL证书名字
```
***下文中的主机名（host name）代指hostname或domain，代表附加到证书上的主机名***
SSL证书必须与一个或多个主机名关联（host name）。所以选择正确的名字非常重要，因为只有当请求与SSL证书关联的主机名匹配时，证书才有效。
此外，证书颁发后，无法更改证书的名称类型（如，从单名类型证书改为通配符名类型证书）。
```

## Single VS Multi names
```
可以使用Common Name(CN)或Subject Alternative Name(SAN)两种方式将你的主机名与SSL证书关联。

CN允许指定单个条目（单名或通配符），SAN扩展则支持多个条目。但是SAN仅受某些SSL证书产品的支持。
```

### Common Name
```
Common Name标识了证书与主机的关联。如：www.example.com
它包含单名证书和通配符证书。注意，它不是URL所以不包含任何协议。
```

#### Single-name vs Wildcard
```
在申请证书前，需要了解单名证书和通配符证书之间的差别。因为它会影响您可以使用单个证书覆盖哪些域。
```

##### Single-name SSL certificate
```
单名证书仅对证书指定的主机名有效。
比如，您有secure.example.com主机的证书，但是您不能用于www.example.com或example.com（浏览器会告警）。
*** 注意 ***
根域是例外的
不管是单名证书还是通配符证书，符合下面条件的可以用于根域名（例如根域：example.com）
1. 对于单名证书，必须用于www子域的证书（例如:www.example.com）。但是如果您为根域购买证书，则无法将其使用于www域。
2. 对于通配符证书，您必须拥有3级域名模式（例如：*.example.com）。
```

##### Wildcard SSL certificate
```
通配符证书仅对单级的子域有效。可以使用通配符'*'表示子域。
比如，您拥有*.example.com的证书，您可以用于www.example.com,shit.example.com等，但是，不能用于shit.shit.example.com等非单级的主机
```

### Subject Alternative Name(SAN)
```
Subject Alternative Name(SAN)是对X.509规范的扩展，允许为单个SSL证书制定其他主机名。
实际上，使用术语“SAN证书”时，我们指的是可以覆盖多个主机名（域）的SSL证书，也称为多域SSL证书（多域证书）
除了语法上有效的主机名外，对SAN扩展可覆盖的主机名没有特殊的限制。但是证书颁发机构可能会根据内部规则或业务决策增加数字或格式的进一步限制。
例如：
	通常不允许任意通配符名称作为SAN主机名。这意味着SAN证书通常只支持一个枚举名称。
	通常为每个证书设置有100个名字的限制（每个证书名字数量限制很常见）。
最后，名称通常不需要属于同一个域。
例如：
	example.com
	foo.bar.hello.com
	another.domain.com
```

#### 背景
```
x.509规范规定了公开密钥认证、证书吊销列表、授权证书、证书路径验证算法等。其中包括了SSL证书格式。最初SSL证书只允许在名为Common Name的证书主题中制定单名。
CN表示SSL证书所覆盖的主机名。尝试将证书用于与名称不匹配的网站将导致安全错误，也称为主机名不匹配错误。
在最初的具体细节之后，显而易见的是，拥有一个证书来覆盖多个主机名是有帮助的。最常见的是包含根域名和www子域的单证书情况。
The X.509 specification allows to define extensions to be attached to a Certificate Signing Request (CSR) and the final server certificate.
使用SAN扩展可以在证书的subjectAltName字段中制定多个主机名，这些名称中每个都将被认为受SSL证书保护。
```
### 名词解析

#### 证书
```
在X.509里，组织机构通过发起证书签名请求（CSR）来得到一份签名的证书。首先需要生成一对密钥对，然后用其中的私钥对CSR进行数字签署（签名），并安全地保存私钥。CSR进而包含有请求发起者的身份信息、用来对此请求进行验真的的公钥以及所请求证书专有名称。CSR里还可能带有CA要求的其它有关身份证明的信息。然后CA对这个CSR进行签名。 组织机构可以把受信的根证书分发给所有的成员，这样就可以使用公司的PKI系统了。浏览器（如Firefox）或操作系统预装有可信任的根证书列表，所以主流CA发布的TLS证书都直接可以正常使用。浏览器的开发者直接影响着它的用户对CA的信任。X.509也定义了CRL实现标准。另一种检查合法性的方式是OCSP。

证书组成结构
证书组成结构标准用ASN.1（一种标准的语言）来进行描述. X.509 v3 数字证书结构如下：
* 证书
	* 版本号
	* 序列号
	* 签名算法
	* 颁发者
	* 证书有效期
		* 此日期前无效
		* 此日期后无效
	* 主题
	* 主题公钥信息
		* 公钥算法
		* 主题公钥
	* 颁发者唯一身份信息（可选项）
	* 主题唯一身份信息（可选项）
	* 扩展信息（可选项）
		* ...
* 证书签名算法
* 数字签名

扩展指定了证书的用途
RFC 5280（及后续版本）定义了一些扩展用来指定证书的用途。 它们的多数都来源于joint-iso-ccitt(2) ds(5) id-ce(29) OID。在4.2.1里定义的几个常用扩展定义如下：

Basic Constraints， { id-ce 19 }[4] 用于指定一份证书是不是一个CA证书。
Key Usage, { id-ce 15 },[5]指定了这份证书包含的公钥可以执行的密码操作。作为一个例子，它可以指定只能用于签名，而不能用来进行加密操作。
Extended Key Usage, { id-ce 37 },[6]典型用法是用于叶子证书中的公钥的使用目的。它包括一系列的OID，每一个都指定一种用途。比如{ id-pkix 3 1 } 表示用于服务器端的TLS/SSL连接，而{ id-pkix 3 4 }用于email的安全操作。
通常情况下，一份证书有多个限制用途的扩展时，所有限制条件都应该满足才可以使用。RFC 5280里有对一个同时含有keyUsage和extendedKeyUsage的证书的例子，这样的证书只能用在两个扩展中都指定了的用途。比如网络安全服务决定证书用途时会同时对这两个扩展进行判断[7]

证书文件扩展名
X.509有多种常用的扩展名。不过其中的一些还用于其它用途，就是说具有这个扩展名的文件可能并不是证书，比如说可能只是保存了私钥。

.pem – 隐私增强型电子邮件格式，通常是Base64格式的。
.cer, .crt, .der – 通常是DER二进制格式的。
.p7b, .p7c – PKCS#7 SignedData structure without data, just certificate(s) or CRL(s)
.p12 – PKCS#12格式，包含证书的同时可能还包含私钥
.pfx – PFX，PKCS#12之前的格式（通常用PKCS#12格式，比如由互联网信息服务产生的PFX文件）
PKCS#7 是签名或加密数据的格式标准，官方称之为容器。由于证书是可验真的签名数据，所以可以用SignedData结构表述。 .P7C文件是退化的SignedData结构，没有包括签名的数据。

PKCS#12 由PFX进化而来的用于交换公共的和私有的对象的标准格式。

ex: 
## 创建私钥
openssl genrsa -out private.pem 2048

## 导出公钥
openssl rsa -in private.pem -pubout -out public.pem

## 创建CSR
openssl req -new -key private.pem -out req.csr
### 验证
openssl req -text -in req.csr -noout -verify
### 一条语句生成CSR和私钥
openssl req -new \
	-newkey rsa:2048 -nodes -keyout private.pem \
	-out one_cmd.csr \
	-subj "/C=CN/ST=SiChuan/L=Chengdu/O=self/OU=test/CN=test.self"

## 生成证书
openssl x509 -req -days 3650 -in req.csr -signkey private.pem -out cert.pem

## 一条语句生成证书、私钥
openssl req -new -nodes -utf8 -sha256 -days 36500 -batch -x509 -config x509.genkey -outform PEM -out signing_key.pem -keyout signing_key.pem
其中：
	-out 指定输出名
	-keyout 指定输出私钥的文件名，这儿私钥和证书在一个文件中
	-nodes 如果私钥被创建，将不加密

# 完整示例
## 创建证书颁发机构的证书和密钥
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 365000 \
   -key ca-key.pem \
   -out ca-cert.pem
## 颁发服务端证书
openssl req -newkey rsa:2048 -nodes -days 365000 \
   -keyout server-key.pem \
   -out server-req.pem
openssl x509 -req -days 365000 -set_serial 01 \
   -in server-req.pem \
   -out server-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem
## 颁发客户端证书
openssl req -newkey rsa:2048 -nodes -days 365000 \
   -keyout client-key.pem \
   -out client-req.pem
openssl x509 -req -days 365000 -set_serial 01 \
   -in client-req.pem \
   -out client-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem
## 验证
openssl verify -CAfile ca-cert.pem \
   ca-cert.pem \
   server-cert.pem
```

#### Certificate Signing Request (CSR)
```
证书签名请求（CSR或证书请求），是发送给证书颁发机构以便申请证书的加密文本块。
CSR中包含的信息将包含在您的证书中，如CN、所有者详细信息。还包含将要嵌入到证书中的公钥。
```
#### Certificate Authority(CA)
```
证书颁发机构
```

## ref
* [X.509](https://zh.wikipedia.org/wiki/X.509)
* [goca](https://github.com/kairoaraujo/goca.git)
* [x509.genkey](./x509.genkey)
* [OpenSSL Quick Reference Guide](https://www.digicert.com/kb/ssl-support/openssl-quick-reference-guide.htm)
* [Creating Self-Signed Certificates and Keys with OpenSSL](https://mariadb.com/docs/security/data-in-transit-encryption/create-self-signed-certificates-keys-openssl/)