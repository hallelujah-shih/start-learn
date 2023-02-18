# http client分析

## 核心结构说明
```
http client的核心精髓在于RoundTripper接口，
```

### RoundTripper接口
```
接口声明：
type RoundTripper interface {
	RoundTrip(*Request) (*Response, error)
}
RoundTrip(来回应答器)是执行单个 HTTP 事务，为提供的请求返回响应。
* 必须初始化请求的 URL 和标头字段。

有诸多建议，这儿不再列出，特别想说的是，要做一些特殊的事情，就需要自己实现此接口，而可能突破其中一些建议。
```

#### http.Client的RoundTripper实现分析
```
在Client的Do方法中实现了执行请求的过程，其中若无自定义Transport则使用默认的DefaultTransport（实现了RoundTripper接口）
Transport结构较为复杂，实现了HTTP、HTTPS以及HTTP代理等逻辑，内部包括处理了连接的管理、复用。


```

#### x/net/http2.ClientConn中的RoundTripper实现分析
```
```

### 回调函数接口CheckRedirect
```
函数原型： func(req *Request, via []*Request) error

```

### CookieJar接口
```
接口声明：
type CookieJar interface {
	SetCookies(u *url.URL, cookies []*Cookie)
	Cookies(u *url.URL) []*Cookie
}
```
