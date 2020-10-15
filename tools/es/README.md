# ES
```
es基本操作
```

## 查询更新
```
POST twitter/_update_by_query
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "script": {
    "source": "ctx._source['extra'] = 'test'"
  }
}
```
