# lua基础

## 数据类型
```
数值类型： 整数、浮点

布尔类型： true、false

字符串类型： 单引号或双引号内的内容

自定义类型： 通过自定义类型，可以实现不同语言间的互操作

函数类型： Lua中函数可以作为一种数据类型使用，可以赋值给一个变量或者作为参数传递给其他的函数。
    function func_name(arg_list) {
        ...
        [return xxx]
    }

线程类型：表示一个县城，可以同时执行多个线程，每个线程有自己的独立栈、局部变量和指令指针。

表类型：table实现了一组关联数组类型。使用{}表示
    字典：
        local v1 = {id = "100", name = "lua"}
        local v2 = {["id"]="100", ["name"]="lua"}
        print(v1.id, v2.id)
        print(v1["name"], v2["name"])
    数组:
        local lang = ["lua", "c", "c++"]
        for i, v in ipairs(lang) do
            ...
        end
        for i = 1, #lang do
            ...
        end

nil： 变量没被赋值前的默认值为nil，若变量被赋值为nil，则lua垃圾回收器会删除该变量，释放它所占用的内存。


可以通过type函数获取数据类型，如print(type("Hello Lua"))。
可以通过tostring()将数据转化为字符串，可以通过tonumber()将数据转为数值。
```

## 控制语句
```
结构化程序设计中的控制语句有三种：顺序、分支、循环
Lua中有以下几类
1. 分支： if
2. 循环： while、repeat、for
3. 程序转移相关的跳转语句： break、return
```

### 分支
```
-- if 结构
if <condition> then
    ...
end

-- if ... else 结构
if <condition> then
    ...
else
    ...
end

-- elseif 结构
if <condition-0> then
    ...
elseif <condition-1> then
    ...
.
.
else
    ...
end
```

### 循环
```
-- while
while termination do
    ...
end

-- repeat(与while相似，不过repeat为事后判断)
repeat
    ...
until termination

-- for
for var = start, end, [step=1] do
    ...
end

-- for-in
for i, v in ipairs(a) do
    ...
end
```

### 跳转语句
```
break可用于switch引导的分支结构以及3种循环结构，作用为强行退出循环结构。
return从当前函数中退出。
```

## OO

### metatables & metamethods
```
metatables允许我们改变table的行为，与C++中重载操作符类似。
lua中的每个表都有其metatable，默认创建的表不带metatable
t = {}
print(getmetatable(t)) -- nil
可以使用setmetatable函数设置或者改变一个表的metatable
t1 = {}
setmetatable(t, t1)
assert(getmetatable(t) == t1)
```

#### metamethods: 算术运算
```
+: __add
-: __sub
*: __mul
/: __div
-(负): __unm
**: __pow
```

#### metamethods: 关系运算
```
==: __eq
<: __lt
<=: __le
```

#### metamethods: 库定义
```
转string: __tostring
__metatable: 设置值后getmetatable为设置的值，调用setmetatable会错误
```

#### metamethods: 表相关
```
__index: 在自己实现模块中，比较典型的使用如下：
local _M = {
    _VERSION = "my module version.1"
}

local mt = { __index = _M }

function _M.new(args)
    local new_obj = {}
    ...
    return setmetatable(new_obj, mt)
end

function _M.my_function(self, args)
    ...
end

return _M


__newindex: 用来对表更新，__index则是用来对表访问。
```
