# NGX Module Dev

## Nginx模块的组件
```
一个 Nginx 模块由许多组件组成，这些组件取决于模块的类型。现在我们将讨论几乎所有模块都共有的这些部分。我们的目的是以易于理解的方式向您展示参考资料，使您能够准备好编写自己的模块。
```

### 模块配置
```
模块可以为每个配置文件的配置上下文定义一个配置: 其中main、server、location context都有一个独立的结构。
这些结构应命名为约定 ngx_http_<模块名称>_(main|srv|loc)_conf_t。以下是示例模块中的代码片段：
typedef struct {
    ngx_str_t name;
} ngx_http_hello_loc_conf_t;
这个结构的成员应该和模块指令一样多。 在前面的示例中，我们的模块只有一个指令，因此我们已经知道该模块将在location支持单个指令, 其中指令名赋值给name。 现在很明显，模块配置中的元素由模块配置中定义的模块指令填充。
```

### 模块指令
```
在定义了模块指令的值将被存储的位置之后，是时候定义模块指令的名称以及它们将接受的参数的种类和类型了。 模块的指令在 ngx_command_t 类型结构的静态数组中定义。 查看我们之前编写的示例代码，指令结构如下所示：
static ngx_command_t ngx_http_hello_commands[] = {
    {
        ngx_string("hello"),
        NGX_HTTP_LOC_CONF|NGX_CONF_TAKE1,
        ngx_conf_set_str_slot,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_hello_loc_conf_t, name),
        &ngx_http_hello_p 
    },
    ngx_null_command
};
第一个参数定义指令的名称。 这是 ngx_str 类型，并使用指令名称实例化，例如 ngx_str("hello")。
第二个参数定义了指令的类型，以及它接受的参数类型。 这些参数的可接受值应该相互按位排序。 可能性如下：
    NGX_HTTP_MAIN_CONF: 指令用于 main
    NGX_HTTP_SRV_CONF : 指令用于 server
    NGX_HTTP_LOC_CONF : 指令用于 location
    NGX_HTTP_UPS_CONF : 指令用于 upstream
    NGX_CONF_NOARGS ： 指令不带任何参数
    NGX_CONF_TAKE1 : 指令带1个参数
    NGX_CONF_TAKE2 : 指令带2个参数
    NGX_CONF_TAKE7 : 指令带7个参数
    NGX_CONF_TAKE12 : 指令带1个或2个参数
    NGX_CONF_TAKE13 : 指令带1个或3个参数
    NGX_CONF_TAKE23 : 指令带2个或3个参数
    NGX_CONF_TAKE123 : 指令带1个或2个或3个参数
    NGX_CONF_TAKE1234 : 指令带1个或2个或3个或4个参数
    NGX_CONF_FLAG : 指令接受一个bool值 "on"|"off"
    NGX_CONF_1MORE : 指令至少需要1个参数
    NGX_CONF_2MORE : 指令至少需要2个参数
第三个参数是一个函数指针。这是一个设置函数，它采用为配置文件中的指令提供的值并将其存储在结构的适当元素中。此函数可以采用以下三个参数：
    • 指向ngx_conf_t（main、srv或loc）结构的指针，其中包含配置文件中指令的值
    • 指向将存储值的目标ngx_command_t结构的指针
    • 指向模块自定义配置结构的指针（可以为NULL）
    Nginx 提供了许多可用于设置内置数据类型值的函数。这些功能包括：
        ngx_conf_set_flag_slot ： 将"on"|"off"转为 1 | 0
        ngx_conf_set_str_slot : 将字符串保存为 ngx_str_t
        ngx_conf_set_str_array_slot
        ngx_conf_set_keyval_slot
        ngx_conf_set_num_slot : 分析并保存为整型
        ngx_conf_set_size_slot : 将5k、2m等转为size_t
        ngx_conf_set_off_slot
        ngx_conf_set_msec_slot
        ngx_conf_set_sec_slot
        ngx_conf_set_bufs_slot
        ngx_conf_set_enum_slot
        ngx_conf_set_bitmask_slot
        如果内置函数不足以满足目标，例如，如果字符串需要以某种方式解释而不是仅仅按原样存储，模块作者也可以在此处将指针传递给他们自己的函数。
        为了指定这些内置（或自定义）函数将存储指令值的位置，您必须指定 conf 和 offset 作为接下来的两个参数。 conf指定了值将被存储的结构的类型（main、srv、loc）而offset指定了将其存储在这个配置结构的哪一部分。下面是该结构中元素的偏移量，即offsetof （ngx_http_hello_loc_conf_t, name）。
```

### 模块上下文
```
Nginx 模块中需要定义的第三个结构是静态的 ngx_http_module_t 结构，它只有用于创建 main、srv 和 loc 配置并将它们合并在一起的函数指针。 它的名字是 ngx_http_<module name>_module_ctx。 您可以提供的函数参考如下：
    • 预配置 [ngx_int_t (*preconfiguration)(ngx_conf_t *cf)]
    • 后配置 [ngx_int_t (*postconfiguration)(ngx_conf_t *cf)]

    • 创建main conf [void *(*create_main_conf)(ngx_conf_t *cf)]
    • 初始化main conf [char *(*init_main_conf)(ngx_conf_t *cf, void *conf)]

    • 创建server conf [void *(*create_srv_conf)(ngx_conf_t *cf)]
    • 将其与main conf合并 [char *(*merge_srv_conf)(ngx_conf_t *cf, void *prev, void *conf)]

    • 创建location conf [void *(*create_loc_conf)(ngx_conf_t *cf)]
    • 将其与server conf合并 [char *(*merge_loc_conf)(ngx_conf_t *cf, void *prev, void *conf)]
    在合并期间，如果配置作者在配置文件中提供的指令有问题，模块作者可以查找元素的重复定义并抛出错误。
    大多数模块只使用最后两个元素：一个为 ngx_loc_conf（main、srv 或 loc）配置分配内存的函数，以及一个设置默认值并将此配置合并到合并位置配置（称为 ngx_http_<module name>_merge_loc_conf）。
    如果可以定义多个指令，则通常需要合并函数。
```

### 模块定义
```
新模块应该定义的下一个结构是模块定义结构或 ngx_module_t 结构。 该变量称为 ngx_http_<module name>_module。 该结构将我们迄今为止定义的结构绑定在一起。
必须提供指向上下文和模块指令结构的指针，以及剩余的回调（退出线程、退出进程等）。如下实例：
ngx_module_t ngx_http_hello_module = {
    NGX_MODULE_V1,
    &ngx_http_hello_module_ctx, /* module context */
    ngx_http_hello_commands, /* module directives */
    NGX_HTTP_MODULE, /* module type */
    NULL, /* init master */
    NULL, /* init module */
    NULL, /* init process */
    NULL, /* init thread */
    NULL, /* exit thread */
    NULL, /* exit process */
    NULL, /* exit master */
    NGX_MODULE_V1_PADDING
};
```

### handler函数
```
在完成所有准备工作和配置结构之后，最后一块拼图是完成所有工作的实际处理函数。其中函数指针的定义如下：
typedef ngx_int_t (*ngx_http_handler_pt)(ngx_http_request_t *r);
```

### 总结: 创建Nginx模块的必要步骤
```
1. 为main、server、location创建模块配置，模式如： ngx_http_<module name>_loc_conf_t。并创建模块指令的静态数组，是结构为ngx_command_t的静态数组，模式为：ngx_http_<module name>_commands。
2. 创建模块上下文, 类型为ngx_http_module_t的静态结构体，模式如： ngx_http_<module name>_module_ctx。
    它有一堆用于设置配置的挂钩。例如，您可以在此处设置后配置挂钩来设置模块的主处理程序。
3. 模块定义，是 ngx_module_t 类型的结构体，模式如： ngx_http_<module name>_module。
    其中.ctx是前面创建的模块上下文的引用，.commands是前面创建的模块命令的引用。
4. 创建处理 HTTP 请求的主模块处理函数。
    此函数还在一系列固定大小的缓冲区中输出响应标头和正文。
```

## NDK使用
```
```
