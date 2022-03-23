# nginx modules dev
```
Nginx配置文件包含4个上下文（context）:
    main
        main context的指令作用于全局
    server
        server context下的指令适用于特定的host/port(服务)
    upstream
        upstream context是为一组后端服务器提供设置的
    location
        location context应用于匹配web服务的位置（locations,如"/", "images"等）

location context会继承它的server context，server context也会从main context继承指令；upstream context是不继承也不赋予别人指令（属性）。

```
## Nginx’s Module概览
```
Nginx模块有3个重要角色：
    handlers： 处理请求并产生输出
    filters： 操作/操纵handler处理请求所产生的输出
    load-balancers： 对后端服务器进行合理的选择

典型的处理周期：
    Client sends HTTP request → Nginx chooses the appropriate handler based on the location config → (if applicable) load-balancer picks a backend server → Handler does its thing and passes each output buffer to the first filter → First filter passes the output to the second filter → second to third → third to fourth → etc. → Final response sent to client

调用是通过一系列的回调函数来进行的，而且还有很多：
    在读取server的配置文件之前
    在location和server的每个配置指令
    当Nginx初始化main的配置文件
    当Nginx初始化server的配置文件
    当Nginx为main配置合并server配置时
    当Nginx初始化location配置时
    当Nginx为server配置合并location配置时
    当Nginx的master进程运行时
    当一个新的worker进程运行时
    当一个worker退出时
    当master进程退出时
    处理请求（handling a request）
    过滤响应头
    过滤响应体
    选择后端服务
    向后端服务发起请求
    重新向后端服务发起请求
    处理来自后端服务器的响应
    完成与后端服务器的交互

```

## Nginx module组件

### Module配置结构体
```
模块最多可以定义3个配置结构体，分别作用于main，server，location的上下文。大多数模块之需要一个location配置。其中命名约定为：
ngx_http_<module_name>_(main|srv|loc)_conf_t

比如dav的配置(src/http/modules/ngx_http_dav_module.c)：
typedef struct {
    ngx_uint_t  methods;
    ngx_uint_t  access;
    ngx_uint_t  min_delete_depth;
    ngx_flag_t  create_full_put_path;
} ngx_http_dav_loc_conf_t;

```
### Module指令
```
模块的指令出现在 ngx_command_t 的静态数组中，如dav的指令集：
static ngx_command_t  ngx_http_dav_commands[] = {

    { ngx_string("dav_methods"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_LOC_CONF|NGX_CONF_1MORE,
      ngx_conf_set_bitmask_slot,
      NGX_HTTP_LOC_CONF_OFFSET,
      offsetof(ngx_http_dav_loc_conf_t, methods),
      &ngx_http_dav_methods_mask },

    { ngx_string("create_full_put_path"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_LOC_CONF|NGX_CONF_FLAG,
      ngx_conf_set_flag_slot,
      NGX_HTTP_LOC_CONF_OFFSET,
      offsetof(ngx_http_dav_loc_conf_t, create_full_put_path),
      NULL },

    { ngx_string("min_delete_depth"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_LOC_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_HTTP_LOC_CONF_OFFSET,
      offsetof(ngx_http_dav_loc_conf_t, min_delete_depth),
      NULL },

    { ngx_string("dav_access"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_LOC_CONF|NGX_CONF_TAKE123,
      ngx_conf_set_access_slot,
      NGX_HTTP_LOC_CONF_OFFSET,
      offsetof(ngx_http_dav_loc_conf_t, access),
      NULL },

      ngx_null_command
};

其中ngx_command_t定义如下：
struct ngx_command_s {
    ngx_str_t             name;
    ngx_uint_t            type;
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    ngx_uint_t            conf;
    ngx_uint_t            offset;
    void                 *post;
};

name: 指令名（不能有空格）
type: 指示指令在哪里时合法的以及需要多少参数（bit位）
set: set指向用于设置模块配置的函数的指针，遇到指令时将调用此函数
    一些转化函数(更多参见core/ngx_conf_file.h)：
        ngx_conf_set_flag_slot: 将"on"或"off"转为1或0
        ngx_conf_set_str_slot: 将一个string保存为ngx_str_t
        ngx_conf_set_num_slot: 分析数字并存储为int
        ngx_conf_set_size_slot: 分析数据大小（1m, 8k等）并存储为size_t
conf: 确定配置值存到哪儿
         NGX_HTTP_MAIN_CONF_OFFSET: main context
         NGX_HTTP_SRV_CONF_OFFSET: server context
         NGX_HTTP_LOC_CONF_OFFSET: location context
offset: 指定要写入此配置结构的哪部分
post: 常规性为NULL
```
### 模块上下文
```
上下文由ngx_http_module_t结构体，命名规范是ngx_http_<module name>_module_ctx，结构体定义如下：
typedef struct {
    ngx_int_t   (*preconfiguration)(ngx_conf_t *cf);
    ngx_int_t   (*postconfiguration)(ngx_conf_t *cf);

    void       *(*create_main_conf)(ngx_conf_t *cf);
    char       *(*init_main_conf)(ngx_conf_t *cf, void *conf);

    void       *(*create_srv_conf)(ngx_conf_t *cf);
    char       *(*merge_srv_conf)(ngx_conf_t *cf, void *prev, void *conf);

    void       *(*create_loc_conf)(ngx_conf_t *cf);
    char       *(*merge_loc_conf)(ngx_conf_t *cf, void *prev, void *conf);
} ngx_http_module_t;
```

### 模块定义
```
nginx中是通过ngx_module_t结构体表示，命名规范为ngx_http_<module name>_module，主要设置模块类型、指令、上下文以及一些进程、线程启动退出的一些控制
```
### 模块安装
```
取决于模块是handler、filter、load-balancer，他们有所不同
```
## Handlers
## Filters
## Load-Balancers
## ref
[nginx-modules-guide](https://www.evanmiller.org/nginx-modules-guide.html)
