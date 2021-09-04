# SELINUX
```
一些selinux碰到的问题记录与解决
```

## 恢复文件默认的SELinux security contexts
```
例如，修改了系统配置文件的时候可能改变了文件属性
> sudo restorecon -FRv /etc/crontab
```

## deamon.tools的selinux问题
```
参见../../service_manager/daemon.tools.md
```

## openvpn使用本地目录引发的权限问题
```
现象:在网络管理处import了自己的openvpn配置之后，连接时，提示不能连接，通过journalctl查看，知道了是openvpn使用证书相关文件时没有权限
audit[28485]: AVC avc:  denied  { open } for  pid=28485 comm="openvpn" path="/home/shih/xxxxx
然后执行
> sudo ausearch -m avc --start recent
type=AVC msg=audit(1544879292.428:335): avc:  denied  { open } for  pid=10592 comm="openvpn" path="/home/shih/.shit/users.pem" dev="dm-2" ino=16540126 scontext=system_u:system_r:openvpn_t:s0 tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0
由于直接通过chcon设置type，selinux会告诉你没权限（selinux过于复杂，使用不多，所以下面是我非常规操作结果，有更好的流程，有人知道的可以给我发送邮件告知）
> sudo setenforce 0
> chcon -u system_u -r system_r -t openvpn_t -R .shit/
> sudo setenforce 1

或者是直接
grep openvpn /var/log/audit/audit.log | audit2allow -M myvpn
semodule -i myvpn.pp

然后就可以使用vpn进行友好连接了
```

