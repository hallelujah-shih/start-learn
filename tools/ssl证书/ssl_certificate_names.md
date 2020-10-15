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
#### Certificate Signing Request (CSR)
```
证书签名请求（CSR或证书请求），是发送给证书颁发机构以便申请证书的加密文本块。
CSR中包含的信息将包含在您的证书中，如CN、所有者详细信息。还包含将要嵌入到证书中的公钥。
```
#### Certificate Authority(CA)
```
证书颁发机构
```
