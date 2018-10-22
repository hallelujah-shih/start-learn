# 推荐的日志库
```
github.com/lestrrat-go/file-rotatelogs
github.com/rifflock/lfshook
github.com/sirupsen/logrus
```

## rotatelogs
```
定期处理应用程序的日志切割
```

## lfshook
```
针对logrus的本地文件系统的钩子
```

## 示例
```go
	if null, err := os.OpenFile(os.DevNull, os.O_APPEND|os.O_WRONLY, os.ModeAppend); err != nil {
		fmt.Println("open dev null error:", err)
	} else {
		logrus.SetOutput(bufio.NewWriter(null))
	}

	debugLog := path.Join(cfg.LogDir, "debug.log")
	accessLog := path.Join(cfg.LogDir, "access.log")
	errLog := path.Join(cfg.LogDir, "error.log")

	debugWriter, err := rotatelogs.New(
		debugLog+".%Y%m%d%H",
		rotatelogs.WithLinkName(debugLog),
		rotatelogs.WithMaxAge(24*time.Hour),
		rotatelogs.WithRotationTime(1*time.Hour),
	)
	if err != nil {
		fmt.Println("init debug log error:", err)
		os.Exit(-1)
	}

	accessWriter, err := rotatelogs.New(
		accessLog+".%Y%m%d%H",
		rotatelogs.WithLinkName(accessLog),
		rotatelogs.WithMaxAge(7*24*time.Hour),
		rotatelogs.WithRotationTime(1*time.Hour),
	)
	if err != nil {
		fmt.Println("init access log error:", err)
		os.Exit(-1)
	}

	errWriter, err := rotatelogs.New(
		errLog+".%Y%m%d%H",
		rotatelogs.WithLinkName(errLog),
		rotatelogs.WithMaxAge(30*24*time.Hour),
		rotatelogs.WithRotationTime(1*time.Hour),
	)
	if err != nil {
		fmt.Println("init error log error:", err)
		os.Exit(-1)
	}

	hook := lfshook.NewHook(lfshook.WriterMap{
		logrus.DebugLevel: debugWriter,
		logrus.InfoLevel:  accessWriter,
		logrus.WarnLevel:  errWriter,
		logrus.ErrorLevel: errWriter,
		logrus.FatalLevel: errWriter,
		logrus.PanicLevel: errWriter,
	}, &logrus.TextFormatter{})
	logrus.AddHook(hook)
```
