# Ubuntu的一些杂项

## apt update操作证书问题
```
错误消息:
Err:5 https://mirrors.ustc.edu.cn/ubuntu focal Release
  Certificate verification failed: The certificate is NOT trusted. The certificate chain uses expired certificate.  Could not handshake: Error in the certificate verification. [IP: 202.141.160.110 443]

忽略双向验证:
echo 'Acquire::https::mirrors.ustc.edu.cn::Verify-Peer "false";' > /etc/apt/apt.conf.d/99ustc-cert

重新执行: apt update
```
