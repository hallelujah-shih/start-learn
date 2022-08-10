# 关于一些TLS的DEBUG技巧和工具集介绍

## wireshark
### 使用证书解码
```
这儿不做更多详细的说明，可以见reference 1

edit -> preferences -> protocols -> ssl: rsa keys list
```
### 不使用证书解码
```
通过设置SSLKEYLOGFILE来导出
格式为如下之一:
RSA <space> <16 bytes of hex encoded encrypted pre master secret> <space> <96 bytes of hex encoded pre master secret>

CLIENT_RANDOM <space> <64 bytes of hex encoded client_random> <space> <96 bytes of hex encoded master secret>

主要说明下这种方式
1. WIN 
在环境变量中创建SSLKEYLOGFILE的变量，值为存储key log的路径

2. Linux
echo $SSLKEYLOGFILE，如果没有值 export SSLKEYLOGFILE=/tmp/keylog.txt
我机器为Fedora 22
启动chrome浏览器
/opt/google/chrome/chrome

在wireshark中设置key log路径
edit -> preferences -> protocols -> ssl: (Pre)-Master-Secret log filename: /tmp/keylog.txt
```

### 优劣
```
使用证书解密：
缺点是需要证书，且不支持Diffie-Hellman加密算法

SSLKEYLOGFILE
没有过多限制(chrome,firefox,新版ie支持)
```

## openssl
```
创建RSA KEY和证书对
> openssl req -new -x509 -out server.crt -nodes -keyout server.pem -subj /CN=localhost
> ls
  server.crt  server.pem

通过openssl运行https服务
> openssl s_server -www -cipher AES256-SHA -key server.pem -cert server.crt

通过openssl客户端连接并请求
> printf 'GET / HTTP/1.0\r\n\r\n' | openssl s_client -ign_eof -connect localhost:4433

通过证书认证登陆
# 创建自签名证书
> openssl req -new -x509 -nodes -out client.crt -keyout client.key -subj /CN=Moi/O=Foo/C=NL
# 重启openssl的server服务
> openssl s_server -cipher AES256-SHA -accept 4443 -www -CAfile client.crt -verify 1 -key server.pem -cert server.crt
# 客户端请求
> printf 'GET / HTTP/1.0\r\n\r\n' | openssl s_client -ign_eof -connect localhost:4443 -key client.key -cert client.crt
```

## 使用openssl的应用程序
```
通过GDB得到master_key或client_random
session->master_key
client_random

这个我并没有验证过
详细步骤参见链接:
http://security.stackexchange.com/questions/80158/extract-pre-master-keys-from-an-openssl-application
```

## 批量分析加密数据
```
pcapng格式的dsb块可以解决需要用wireshark去查看数据包的问题
editcap --inject-secrets tls,keys.txt in.pcap out-dsb.pcapng
tshark -r out-dsb.pcapng
或者用pyshark等手动写分析工具
```

## REFERENCE
1. [如何通过wireshark查看HTTPS、HTTP/2网络包](http://joji.me/zh-cn/blog/walkthrough-decrypt-ssl-tls-traffic-https-and-http2-in-wireshark)
2. [wireshark wiki ssl](https://wiki.wireshark.org/SSL)
3. [how to capture and decode h2 traffic with wireshark](https://vanwilgenburg.wordpress.com/2015/11/22/how-to-capture-and-decode-http2-traffic-with-wireshark/)
4. [debugging https or ssl connections to a third party](http://news.gtmtech.co.uk/blog/2013/01/25/debugging-https-or-ssl-connections-to-a-third-party/)
5. [NSS Key Log format](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Key_Log_Format)
6. [using-the-pre-master-secret](https://wiki.wireshark.org/TLS#using-the-pre-master-secret)
