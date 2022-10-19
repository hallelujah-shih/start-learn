# grub
```
基本使用
```

## default
```
1. 修改grub(/etc/default/grub)
    * 项是从0开始的，比如我的环境如下：
menuentry xxx1 {
    ...	
}
submenu xxx2 {
	menuentry ooo1 {
		...
	}
	menuentry ooo2 {
		...
	}
	menuentry ooo3 {
		...
	}
	menuentry ooo4 {
		...
	}
	menuentry ooo5 {
		...
	}
	menuentry ooo6 {
        ...
	}
}

    如若我要选择ooo5，那么我的配置应该为： GRUB_DEFAULT="1>4"

2. 更新grub
    update-grub2
```

## ref
* [default](https://www.gnu.org/software/grub/manual/grub/html_node/default.html#default)