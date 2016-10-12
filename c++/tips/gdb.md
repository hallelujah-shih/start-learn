# gdb tips
```
收录一些debug技巧
```

## 使用GDB的面板
[依赖项目gdb-dashboard](https://github.com/cyrus-and/gdb-dashboard)

## 使用全局的.gdbinit和项目.gdbinit
```
可以在根目录($HOME/.gdbinit)设置全局的gdb配置

在当前工作目录(./.gdbinit)设置项目特殊的gdb配置

NOTE: 必须设定允许项目的特殊.gdbinit； 
    auto-load local-gdbinit
```

## 使用别名
```
在.gdbinit中声明
alias -a w = dashboard expression watch
```

## 使用 $variables
```
(gdb) p str
$1 = "hell oworldafsd"
(gdb) p $1
$2 = "hell oworldafsd"
(gdb) 
```

## 打印指定个数的数组数据
```
C风格的数组
>>> print *Array@10
```

## 启用命令的历史记录
```
在.gdbinit中设置
set history save on
```

## 代码中检查是否由调试器在运行
```
Windows 程序(https://msdn.microsoft.com/en-us/library/windows/desktop/ms680345(v=vs.85).aspx)

类Unix系统

#ifndef _WIN32
#include <sys/ptrace.h>
static int IsDebuggerPresent()
{
    static int Detected;
    static int RunningUnderDebugger;
    if (!Detected)
    {
        Detected = 1;
        RunningUnderDebugger = ptrace(PTRACE_TRACEME, 0, 0, 0) == -1;
    }
    return RunningUnderDebugger;
}
#endif
```

## reference
[Tips for Productive Debugging with GDB](https://metricpanda.com/tips-for-productive-debugging-with-gdb)
