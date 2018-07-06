# ansible
```
一些ansible的简单使用备注
```

## 批量管理公钥
```
authorized_key模块

比如添加某人的key到一批机器上
ansible lvs -m authorized_key -a "key='ssh-rsa AA.....' user=root"
比如删除某人的key
ansible lvs -m authorized_key -a "key='ssh-rsa AA.....' user=root state=absent"
```

## copy文件到远端
```
常用的包括
backup: 是否备份，默认是no
dest: 如果src是目录，这个也必须是目录，注意copy文件时，目标目录不存在的情况
src:
mode:设置文件属性
group:设置分组
owner:设置owner
```
