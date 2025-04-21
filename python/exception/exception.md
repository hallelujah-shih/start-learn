# exception tips

## 设置全局异常处理器
```
用来补锅特别好，不设置，默认就到了终端输出。

比如线上出现过一次python的，通过 os.fork 来处理的 master-slave 架构的程序，
看代码实现，try ... catch Exception 包裹着整个master和slave的执行范围，但是
线上报告程序异常，现象就是 slave 全跪了。

先不论程序本身，因为各种信息不足，没办法真正发现异常出发条件，所以用 sys.excepthook 来进行补锅。保证 master-slave 架构的程序，在发生一些 Exception 不能捕获的异常也能正常将异常信息输出到指定的地方（stdout和stderr被重定向到了 /dev/null）
```