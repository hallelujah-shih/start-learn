# IntelliJ IDEA markdown文件预览中文不能正常显示的问题解决
```
此处以Fedora 32为例，其他系统类似
```

## 操作过程
```
1. 打开 Settings -> Languages & Frameworks -> Markdown
2. 选择 Preview browser: JavaFX WebView
3. Add CSS rules:
    body {
        font-family: 'Noto Sans CJK TC', arial, sans-serif;
    }
    code {
        font-family: 'Noto Sans CJK TC', arial, sans-serif, monospace ;
    }

```

## 如何选择font-family
```
1. 打开terminal并查看系统已安装的中文字体
    fc-list :lang=zh

    我系统输出如下(此处只选一条):
        /usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc: Noto Sans CJK TC,Noto Sans CJK TC DemiLight:style=DemiLight,Regular
```

## 参考
    [系统安装字体查看](https://www.cyberciti.biz/tips/quickly-list-all-available-fonts.html)
    [在线系统字体示例](https://developer.mozilla.org/zh-CN/docs/Web/CSS/font-family)
