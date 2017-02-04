# 简单spark-streaming使用
```
此示例network_wordcount.py中包含了统计计数
技术点包含如下：
1. checkpoint
2. updateStateByKey的使用，特别是可以自定义结构，构建复杂的统计更新
```
## 运行
```
在一个新窗口中运行python raw_sockt_server.py用于生产数据
提交spark任务
> ${SPARK_HOME}/bin/spark-submit network_wordcount.py localhost 9999
```

## 引用
[pyspark streaming使用](https://www.endgame.com/blog/streaming-data-processing-pyspark-streaming)
