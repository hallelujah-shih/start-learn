# ngx_http_proxy_module模块
```
本模块允许请求pass到另外一个服务器

location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```
