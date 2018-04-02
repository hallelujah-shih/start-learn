# HyperScan入门记录
```
对hyperscan的学习过程做记录
hyperscan分为编译特征和扫描特征
```

## 编译依赖
```
GCC >= v4.8.1
CMake >= 2.8.11
Ragel 6.9
Python 2.7
Boost >= 1.57
Pcap >= 0.8 （只有示例代码使用）

cmake可以通过BOOST_ROOT指定非系统的boost目录或ln -s boost_1_59_0/boost <hyperscan-source-path>/include/boost

CMake选项（-D<variable-name>=<value>）非全部
CMAKE_INSTALL_PREFIX
CMAKE_BUILD_TYPE（包括Debug,Release,RelWithDebInfo,MinSizeRel,默认为RelWithDebInfo）
BUILD_SHARED_LIBS（编译动态库代替静态库）
BUILD_STATIC_AND_SHARED（同时编译动态库和静态库）
BOOST_ROOT（可以自己指定boost目录，可能系统默认版本较低，如1.48.0）
DEBUG_OUTPUT（默认未开启，可以打印详细的调试信息）
FAT_RUNTIME（Linux系统上默认为true，其他为false）

特别注意，可以对指定架构进行编译（支持高级指令集，需要了解）,如
cmake -DMAKE_C_FLAGS="-march=corei7" -DCMAKE_CXX_FLAGS="-march=corei7" <hs-source-path>
而使用FAT_RUNTIME的时候自身便打包了不同架构的运行时代码
变种            CPU特性需求           gcc架构标志
Core 2          SSSE3                 -march=core2
Core i7         SSE4_2 and POPCNT     -march=corei7
```

## 编译特征
```
hs的编译器接受正则表达式，并转化为特征数据库，然后可以用于扫描数据
```
### 构造一个数据库
```
hs提供3个API用于将正则编译到数据库中
1. hs_compile() 将单个表达式编译到数据库
2. hs_compile_multi() 将一组表达式编译到数据库。所有提供的模式将在扫描时同事扫描，用户提供的标识符将在匹配时返回
3. hs_compile_ext_multi() 编译一组表达式到数据库，如2，但允许每个表达式指定扩展参数

在编译表达式时，需要确定工作模式是用于流、块还是矢量
流模式(HS_MODE_STREAM): 扫描目标是一个连续的数据流，并不是所有数据都是一次达到。数据块按顺序扫描，匹配可能跨越数据流中的多个块。在此模式下，每个流需要一块内存用于存储扫描调用之间的状态。
块模式(HS_MODE_BLOCK): 一次调用扫描，无中间状态
矢量模式(HS_MODE_VECTORED): 数据一次提供，是非连续块组成，无中间状态

函数参数简单说明:
expressions:
	要编译的，以NULL结尾的表达式数组

flags:
	HS_FLAG_CASELESS: 设置不区分大小写匹配
	HS_FLAG_MULTILINE: ^$可以在多行的行首尾匹配
	HS_FLAG_DOTALL: ‘.’在匹配时会包括换行符
	HS_FLAG_SINGLEMATCH: 设置单一匹配模式
	HS_FLAG_ALLOWEMPTY:
	HS_FLAG_UTF8: 此表达式允许UTF-8模式
	HS_FLAG_UCP: 使用unicode
	HS_FLAG_PREFILTER:在预过滤模式下编译模式
	HS_FLAG_SOM_LEFTMOST: （可能会影响性能）

ids:
	指定要与表达式数组中的相应模式关联的ID数组，若为NULL，会将所有模式的ID设置为0

ext:
	指向hs_expr_ext_t结构体的指针的数组，用于定义每个特征的行为。可以通过指定NULL来表示单个特征不需要扩展行为或者所有特征不需要扩展行为。这些结构使用的内存必须由调用者分配和释放

elements:
	数组的数量

mode:
	HS_MODE_STREAM,HS_MODE_BLOCK,HS_MODE_VECTORED

platform:
	可以指定平台，或者直接NULL

db:
	若成功则返回数据库的指针，否则为NULL。最后须要使用hs_free_database释放内存

error:
	若编译错误，此hs_compile_error_t结构的指针将会被返回，最后需要调用hs_free_compile_error释放内存
```
### 特征支持
```
参见pcre，这里只列出不支持的构造

不支持构造
* 反向引用和捕获子表达式
* 任意的0宽度断言
* 子程序引用和递归模式
* 条件模式
* 回溯控制动词（Backtracking control verbs.）
* \C "单字节"指令（这会打破UTF-8的序列）
* \R 换行
* \K 开始匹配重置指令
* 标注和嵌入代码
* 原子分组和占有量词

与libpcre语义有偏离语义如下
1. 多重匹配模式
2. 缺乏有序
3. 结束偏移：hs默认只报告匹配的结束偏移，在模式编译时可以使用per-expression标志来启用起始偏移的报告
4. “所有”匹配: 如/foo.*bar/对fooxyzbarbar会返回两个匹配结果
```

## 扫描特征
```
hs提供3种不同的扫描模式，每个都有自己的扫描功能，并以hs_scan开头。另外流模式有多个API用于管理流状态
```

### 处理匹配
```
当匹配的时候，将调用用户提供的回调函数，签名如下
typedef int(*match_event_handler)(unsigned int id, unsigned long long from, unsigned long long to, unsigned int flags, void *context)
当此回调函数返回非0时，就可以停止扫描功能了
```
### 流、块、矢量模式
```
流模式
	hs流模式的核心API包括hs_open_stream(),hs_scan_stream(),hs_close_stream()，特别要注意匹配细节，参见官方文档

	流管理
		包括hs_reset_stream(),hs_copy_stream(),hs_reset_and_copy_stream()
	流压缩
		包括hs_compress_stream(),hs_expand_stream(),hs_reset_and_expand_stream()
块模式
	只有一个函数hs_scan(),类似调用hs_open_stream(),hs_scan_stream(),hs_close_stream()
矢量模式
	只有一个函数hs_scan_vector()
```

### 其他
```
当hs扫描数据，需要一些内存用于存储内部信息，特别是对于嵌入式程序来说，栈空间太小，所以需要预先分配内存
分配函数为hs_alloc_scratch，值得注意的是，若程序使用多个数据库时，会用同一片区域，所以需要保证多数据库的情况下空间是否充足
特别注意，虽然hs库可重入，但是临时空间(scratch space)是不可重入的,在没递归扫描的情况下，每个线程只需要一个这样的空间，并做提前分配
在farm模式中,master只做编译，可以通过hs_alloc_scratch()将临时空间copy到所有线程中

也可以自定义分配函数，细节可以参见官方文档
```

## 序列化
```
希望database提前编译，然后将数据库分发，需要甬道序列化和反序列化，有需要的可以详细查看文档（工程上用得上）
```

## 性能考虑
```
1. 正则表达式构建
	* 不要手工优化正则表达式结构
2. 库使用
	* 不要手动优化库的使用
3. 基于块的匹配
	* 在可能的情况下，优先选择基于块的匹配。
4. 不必要的数据库
	* 避免不必要的“联合”数据库（注意，这个可能会反程序狗直觉，慎重慎重）
5. 提前分配临时空间(scratch space)
	* 应该在特征数据库编译完整或者是反序列化完成后就调用hs_alloc_scratch，而不是在每次执行扫描函数前
6. 为每个扫描上下文分配一个临时空间
	* 每个并发扫描操作（如线程）都需要自己的临时空间
		hs_alloc_scratch支持在现有的临时空间上“增加”,如下示例显示将多个db放入同一个临时空间中
		hs_database_t *db1 = build_db1();
		hs_database_t *db2 = build_db2();
		hs_database_t *db3 = build_db3();

		hs_error_t err;
		hs_scratch_t *scratch = NULL;
		err = hs_alloc_scratch(db1, &scratch);
		check_error(err);
		err = hs_alloc_scratch(db2, &scratch);
		check_error(err);
		err = hs_alloc_scratch(db3, &scratch);
		check_error(err);
		// 后续就可以用scratch到扫描中了，或者是hs_clone_scratch来使用scratch了
7. 锚定特征
	* 如果特征出现在数据开始出，请确保将特征锚定
		比如/^foo/这种，细节请参见官方文档
8. 避免无处不在的匹配（配合7理解）
9. 流媒体模式下的有界重复（是昂贵的，决定使用的时候需要详细查看文档）
10. 对于文字匹配更偏好（越长的文字越好，比如/b\w*foobar/就没有/blah\w*foobar/好）
11. 尽可能使用“dot all”模式（HS_FLAG_DOTALL）
```


