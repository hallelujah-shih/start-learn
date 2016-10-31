# C++实现的一个紧凑有限状态机
```
C++有限状态机练习
```

## 事件
```
事件分为外部事件
外部事件是最基本的层次，是一个函数调用到状态机对象（供外部调用的公共函数）
内部事件是状态执行期间由状态机自身产生的状态

一旦外部事件启动状态机执行，它不能被另外一个外部事件中断，直到外部事件和所有内部事件已经完成执行
```

## reference
[state machine design in c++](http://www.codeproject.com/Articles/1087619/State-Machine-Design-in-Cplusplus)
