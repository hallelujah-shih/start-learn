# 测试使用方式
```
> sudo docker-compose up
> curl "http://localhost:5556/"
> cat log/error.log
```

## 测试结论
```
通过模拟client -> cdn -> upstream发现，如果client的socket关闭的时候，cdn->upstream还在进行，那么得到状态码499
client -> cdn -> client，如果关闭，cdn将会返回正常的状态码，并不能区别是否是client提前关闭
```
