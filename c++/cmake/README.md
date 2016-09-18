# 简单CMake使用介绍
```
现在CMake已经在成为事实上很多项目编译的管理工具了，值得学习。
在今天（2016）cmake的项目占了多数，msbuild,scons,autoconf,automake基本上都有很大的局限性
```

## 简单使用
### 创建CMakeLists.txt
```
cmake_minimum_required(VERSION 3.6)
project(string_test)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp)
add_executable(string_test ${SOURCE_FILES})
```
### 编译&运行
```
> mkdir -p build
> cd build
> cmake ..
> cmake --build .
> ./string_test
```

## CMake语法
* 每一行是一个命令调用
* 命令不会返回值
* 命令不能被嵌套
* 所有的参数都为字符串
* 变量作用域继承父级作用域
* ${<var-name>}这种形式的变量可以被计算
* 控制结构包括: if(...) | elseif(...) | else() | endif(), foreach(...) | endforeach(), while(...) | endwhile(), break(), function(...), endfunction(), return(), ...

## 有用的一些变量
```
UNIX, WIN32, APPLE, MSYS, ...
CMAKE_CURRENT_LIST_DIR
CMAKE_CURRENT_SOURCE_DIR
CMAKE_CURRENT_BINARY_DIR
...
```

## 创建CMake脚本文件
```
filename: fizzbuzz.cmake

function(fizzbuzz last)
    foreach(i RANGE 0 ${last})
        math(EXPR notFizz "${i} % 3")
        math(EXPR notBuzz "${i} % 5")
        if(NOT notFizz AND notBuzz)
            message("fizz")
        elseif(notFizz AND NOT notBuzz)
            message("buzz")
        elseif(NOT notFizz AND NOT notBuzz)
            message("${i}")
        endif()
    endforeach()
endfunction()

fizzbuzz(${n})

> cmake -Dn=15 -P fizzbuzz.cmake
```

## 创建自己的项目
1. CMakeLists.txt是用来描述你项目的
2. 必须以cmake_minimum_required(VERSION x.x)开始（使得cmake可以向后兼容）
3. 必须包含project(<project-name>)
    * 不要假设你的项目是根项目
4. 然后你可以写你自己喜欢的东西了
5. 可以增加你的子项目:add_subdirectory(<dir>)
    * 这允许你轻松创建第归的项目结构
    * Subdirectory必须包含一个CMakeLists.txt
    * 所有的目录计算都是根据当前目录来的
    * 永远不要假设你的项目是个根项目
6. 目标是你的项目依赖图中的一个点，可以是可执行文件、动态库、静态库，只有头文件的lib或自定义
    * add_executable(<name> <sourcefile>...)
      add_library(<name> [SHARED|STATIC|INTERFACE]<sourcefile>...)
      add_custom_target(<name> ...)
      (install)
    * SHARED 创建动态库
    * STATIC 创建静态库
    * INTERFACE 创建只有头文件的库（header only library）
7. 使用一些函数来控制自己的目标
    * target_include_directories(<target-name> [PUBLIC|INTERFACE|PRIVATE] <include-dir>...)增加头文件的查找路径
    * target_compile_definitions(<target-name> [PUBLIC|INTERFACE|PRIVATE] <definition>...) 增加预处理定义
    * target_compile_options(<target-name> [PUBLIC|INTERFACE|PRIVATE] <include-dir>...)增加编译选项（-Wall， /bigobj ,...）
    * target_compile_features(<target-name> [PUBLIC|INTERFACE|PRIVATE] <include-dir>...)增加可能的编译特性(cxx_constexpr, ...)
    * target_sources(<target-name> [PUBLIC|INTERFACE|PRIVATE] <source-file>...)增加更多的源文件
    * target_link_libraries(<target-name> [PUBLIC|INTERFACE|PRIVATE] <other-target>...) 增加依赖库

    * PUBLIC 依赖于它的所有目标都能够使用此属性
        target_include_directories(myTarget PUBLIC ./include)，./include目录会使得myTarget和所有通过target_link_libraries依赖于它的目标都能够找到此目录下的头文件
    * INTERFACE 只有目标依赖于它，此属性才能被使用
        target_include_directories(myTarget PRIVATE ./src), ./src只能被myTarget查找到头文件
    * PRIVATE 只有在当前目标中，此属性才能被使用
        target_compile_definitions(myTarget INTERFACE USE_MYTARGET),预处理定义了USE_MYTARGET会被所有依赖于myTarget的可见，但是myTarget自身不可见
8. 安装指令
    * install(...)
    * install(FILES <file>... DESTINATION <dir>)
    * install(TARGETS <target>... DESTINATION <dir>)
    * install(EXPORT <target> NAMESPACE <name> DESTINATION <dir>)

## reference
[moderncmake](https://github.com/toeb/moderncmake)
[cmake如门](https://zh.wikibooks.org/zh/CMake_%E5%85%A5%E9%96%80)
