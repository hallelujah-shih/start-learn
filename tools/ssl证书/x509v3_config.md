# x509v3 config

## critical or non-critical
```
    证书中的每个证书扩展都被指定为关键(critical)或非关键(non-critical)。 如果使用证书的系统遇到它无法识别的关键扩展或包含它无法处理的信息的关键扩展，则必须拒绝证书。
    一个非关键扩展如果不被识别可以被忽略，但如果它被识别则必须被处理。
```

## 标准扩展

### 基本约束（Basic Constraints）
```
    这是一个多值扩展，指示证书是否为 CA 证书。第一个值是 CA，后跟 TRUE 或 FALSE。如果 CA 为 TRUE，则可以包含一个可选的 pathlen 名称，后跟一个非负值。
    CA 证书必须包含将 CA 参数设置为 TRUE 的 basicConstraints 名称。 最终用户证书必须具有 CA:FALSE 或完全省略扩展。 pathlen 参数指定链中可以出现在此 CA 之下的最大 CA 数。 pathlen 为零意味着 CA 不能签署任何子 CA，并且只能签署最终实体证书。
    示例：
 basicConstraints = CA:TRUE
 basicConstraints = CA:FALSE
 basicConstraints = critical, CA:TRUE, pathlen:1
```

### 密钥用法（Key Usage）
```
    密钥用法是一个多值扩展，由允许的密钥用法的名称列表组成。 定义的值是：
digitalSignature
nonRepudiation
keyEncipherment
dataEncipherment
keyAgreement
keyCertSign
cRLSign
encipherOnly
decipherOnly

    示例：
 keyUsage = digitalSignature, nonRepudiation
 keyUsage = critical, keyCertSign
```

### 扩展密钥用法（Extended Key Usage）
```
此扩展包含一个值列表，指示可以使用证书公钥的目的。 每个值可以是短文本名称或 OID。 以下文本名称及其预期含义是已知的：
 Value                  Meaning according to RFC 5280 etc.
 -----                  ----------------------------------
 serverAuth             SSL/TLS WWW Server Authentication
 clientAuth             SSL/TLS WWW Client Authentication
 codeSigning            Code Signing
 emailProtection        E-mail Protection (S/MIME)
 timeStamping           Trusted Timestamping
 OCSPSigning            OCSP Signing
 ipsecIKE               ipsec Internet Key Exchange
 msCodeInd              Microsoft Individual Code Signing (authenticode)
 msCodeCom              Microsoft Commercial Code Signing (authenticode)
 msCTLSign              Microsoft Trust List Signing
 msEFS                  Microsoft Encrypted File System

    示例：
 extendedKeyUsage = critical, codeSigning, 1.2.3.4
 extendedKeyUsage = serverAuth, clientAuth
```

### 主题密钥标识符（Subject Key Identifier）
```
SubjectKeyIdentifier (SKID) 在 RFC 5280 中定义为 X.509 证书扩展，它提供了一种识别包含特定公钥的证书的方法。

    示例：
subjectKeyIdentifier = hash
```

### 授权密钥标识符（Authority Key Identifier）
```
AuthorityKeyIdentifier在RFC5280中被定义为一个X.509证书扩展，它提供了一种识别与用于签署证书的私钥相对应的公钥的方法。
AuthorityKeyIdentifier扩展用于发行人有多个签署密钥的情况（由于有多个同时存在的密钥对或由于转换）。识别可以基于密钥标识符（签发者证书中的主题密钥标识符）或签发者名称和序列号。

AuthorityKeyIdentifier扩展的keyIdentifier字段必须包含在所有由符合要求的CA生成的证书中，以促进认证路径的构建。
有一个例外；当 CA 以 "自签名 "证书的形式分发其公开密钥时，可以省略 AuthorityKeyIdentifier。自签名证书上的签名是用与该证书主体公钥相关的私钥生成的。(在这种情况下，主体和授权钥匙标识符将是相同的，但只有主体钥匙标识符是需要用于建立认证路径。

keyIdentifier字段的值应从用于验证证书签名的公钥或产生唯一值的方法中导出。

    示例：
authorityKeyIdentifier = keyid, issuer
authorityKeyIdentifier = keyid, issuer:always
```

### 主题备用名称（Subject Alternative Name）
```
这是一个多值扩展，支持几种类型的名称标识符，包括email（电子邮件地址）、URI（统一资源指标）、DNS（DNS域名）、RID（a registered ID: OBJECT IDENTIFIER）、IP（IP地址）、dirName（a distinguished name）和otherName。各自的语法将在下面几段中描述。

email: 
IP: 选项中使用的 IP 地址可以是 IPv4 或 IPv6 格式。
dirName: 值是指定包含要使用的区分名称的配置部分，作为一组名-值对。多值的AVAs可以通过在名称前加一个+字符来形成。
otherName: 的值可以包括与OID相关的任意数据；该值应该是OID后面的分号，内容用ASN1_generate_nconf(3)中的语法指定。

    示例：
subjectAltName = email:copy, email:my@example.com, URI:http://my.example.com/
subjectAltName = IP:192.168.7.1
subjectAltName = IP:13::17
subjectAltName = email:my@example.com, RID:1.2.3.4
subjectAltName = otherName:1.2.3.4;UTF8:some other identifier

[extensions]
subjectAltName = dirName:dir_sect

[dir_sect]
C = UK
O = My Organization
OU = My Unit
CN = My Name

符合 RFC 6531 第 3.3 节中定义的语法的非 ASCII 电子邮件地址作为 otherName.SmtpUTF8Mailbox 提供。根据 RFC 8398，电子邮件地址应提供为 UTF8String。为了执行证书中的有效表示，SmtpUTF8Mailbox 应按以下方式提供

    示例：
subjectAltName=@alts
[alts]
otherName = 1.3.6.1.5.5.7.8.9;FORMAT:UTF8,UTF8String:nonasciiname.example.com
```

### 发行人备用名称（Issuer Alternative Name）
```
此扩展支持大多数subject alternative name选项；它不支持email:copy。它还将 issuer:copy 添加为允许的值，如果可能，它会从颁发者证书复制任何主题备用名称。

    示例：
issuerAltName = issuer:copy
```

### 授权信息访问（Authority Info Access）
```
这个扩展给出了如何检索与 CA 提供的证书有关的信息的细节。语法是access_id;location，其中access_id是一个对象标识符（尽管只有少数值是众所周知的），location的语法与subject alternative name相同（除了不支持email:copy）。

access_id的可能值包括OCSP（OCSP responder）、caIssuers（CA Issuers）、ad_timestamping（AD Time Stamping）、AD_DVCS（ad dvcs）、caRepository（CA Repository）。

    示例：
authorityInfoAccess = OCSP;URI:http://ocsp.example.com/,caIssuers;URI:http://myca.example.com/ca.cer
authorityInfoAccess = OCSP;URI:http://ocsp.example.com/
```

## REF
* [x509v3 config](https://www.openssl.org/docs/manmaster/man5/x509v3_config.html)
* [key usage extension](https://superuser.com/questions/738612/openssl-ca-keyusage-extension)
* [certificate extensions](https://ldapwiki.com/wiki/Certificate%20Extensions)