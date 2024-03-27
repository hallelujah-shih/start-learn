# systemd
```
Systemd 管理所谓的单元，它们是系统资源和服务的表示。以下列表显示了 systemd 可以管理的单元类型：
service
    系统上的服务，包括启动、重新启动和停止服务的说明。
socket
    与服务关联的网络套接字。
device
    专门由 systemd 管理的设备。
mount
    由 systemd 管理的挂载点。
automount
    启动时自动挂载。
swap
    系统的交换空间。
target
    其他单元的同步点。通常用于在引导时启动启用的服务。
path
    基于路径的激活的路径。例如，您可以根据某个路径的状态（例如是否存在）来启动服务。
timer
    用于另一个单元的激活的计时器。
snapshot
    当前 systemd 状态的快照。通常用于对 systemd 进行临时更改后回滚。
slice
    通过 Linux 控制组节点 (cgroup) 限制资源。
scope
    来自 systemd 总线接口的信息。通常用于管理外部系统进程。
```

## 服务基本管理
```
systemctl start | stop | restart | reload |enable | disable | status | mask | is-enabled | ...
```
## 修改
```
systemctl edit httpd.service
带 --full 选项，直接完全替换配置文件
```
## 创建新的服务
```
vim /etc/systemd/system/foo.service
[Unit] 部分提供有关服务的基本信息。
    Description 描述单位的字符串。 Systemd 在用户界面中的单元名称旁边显示此描述。
    Documentation 以空格分隔的 URI 列表，引用此服务或其配置的文档。仅接受以下类型的 URI：http://、https://、file:、info:、man:。
    Requires 配置对其他服务的需求依赖性。如果此服务被激活，此处列出的单位也会被激活。
    Wants 与 Requires 类似，但失败的单元不会对服务产生任何影响。
    BindsTo 与 Requires 类似，不同之处在于停止依赖单元也会停止服务。
    PartOf 与 Requires 类似，不同之处在于停止和重新启动依赖单元也会停止和重新启动服务。
    Conflicts 以空格分隔的单元名称列表，如果这些单元名称正在运行，则会导致服务无法运行。
    Before, After 以空格分隔的单元名称列表，用于配置服务之间依赖关系的顺序。
    OnFailure 当此服务进入失败状态时激活的以空格分隔的单元名称列表。
[Service] 部分提供有关如何控制服务的说明。 foo 服务使用以下参数:
    Type 定义 systemd 服务的类型。
        simple - 服务作为主进程启动。这是默认设置。
            服务进程不会 fork，如果该服务要启动其他服务，不要使用此类型启动，除非该服务是 socket 激活型
        forking - 该服务调用 forked processes 并作为主守护程序的一部分运行。
        oneshot - 与simple类似，只不过进程必须在systemd启动后续服务之前退出。
        dbus - 与 simple 类似，不同之处在于守护进程获取 D-Bus 总线的名称。
        notify - 与 simple 类似，不同之处在于守护进程在启动后使用 sd_notify 或等效调用发送通知消息。
        idle - 与 simple 类似，不同之处在于服务的执行被延迟，直到所有活动作业都被调度为止。
    RemainAfterExit 一个布尔值，指定即使服务的所有进程都退出，服务是否仍应被视为活动的。默认为否。
    GuessMainPID 一个布尔值，指定如果无法可靠地确定服务的主 PID，systemd 是否应该猜测它。除非设置了 Type=forking 并且未设置 PIDFile，否则将忽略此选项。默认为是。
    PIDFile 指向该守护程序的 PID 文件的绝对文件名。对于 Type=forking 的服务，建议使用此选项。Systemd在服务启动后读取守护进程主进程的PID。
    BusName 到达此服务的 D-Bus 总线名称。对于 Type=dbus 的服务，此选项是必需的。
    ExecStart 服务启动时执行的命令和参数。
    ExecStartPre, ExecStartPost 在 ExecStart 中的命令之前或之后执行的其他命令。
    ExecReload 服务重新加载时要执行的命令和参数。
    ExecStop 服务停止时要执行的命令和参数。
    ExecStopPost 服务停止后要执行的其他命令。
    RestartSec 重新启动服务之前休眠的时间（以秒为单位）。
    TimeoutStartSec 等待服务启动的时间（以秒为单位）。
    TimeoutStopSec 等待服务停止的时间（以秒为单位）。
    TimeoutSec 同时配置 TimeoutStartSec 和 TimeoutStopSec 的简写。
    RuntimeMaxSec 服务运行的最长时间（以秒为单位）。传递无穷大（默认值）以配置无运行时间限制。
    Restart 配置当服务的进程退出、被杀死或超时时是否重新启动服务：
        no - 该服务将不会重新启动。这是默认设置。
        on-success - 仅当服务进程完全退出（退出代码 0）时重新启动。
        on-failure - 仅当服务进程退出时重新启动，退出代码不为 0。
        on-abnormal - 如果进程因信号而终止或发生超时，则重新启动。
        on-abort - 如果进程由于未捕获的信号未指定为干净退出状态而退出，则重新启动。
        always - 无条件重启
[Install] 提供有关 systemd 如何安装服务的说明。
    Alias 此服务应安装在以空格分隔的附加名称列表下。此处列出的名称必须具有与服务文件名相同的后缀（即类型）。
    RequiredBy, WantedBy 将服务定义为依赖于另一个服务。这通常定义触发启用的服务运行的目标。这些选项类似于 [Units] 部分中的 Requires 和 Wants。
    Also 安装或卸载此服务时要安装或卸载的其他单元。
 
example:
[Unit]
Description=My custom service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/sleep infinity

[Install]
WantedBy=multi-user.target
```

## example
```
示例1
sudo EDITOR=vim systemctl edit --force --full foo.service

[Unit]
Description=My custom service
After=network.target

[Service]
Type=simple
PIDFile=/tmp/foo-svc.pid
ExecStart=/bin/sleep infinity
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target



sudo systemctl daemon-reload
sudo systemctl start foo.service
不断kill sleep进程，并status看服务状态

示例2
systemctl show -p FragmentPath nginx.service

[Unit]
Description=A high performance web server and a reverse proxy server
Documentation=man:nginx(8)
After=network.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target

执行kill后nginx就灭了，我们将配置中创建一个restart
sudo EDITOR=vim systemctl edit --full nginx.service

RestartSec=1
Restart=always

systemctl daemon-reload
systemctl start nginx.service

示例3
创建自己的slice
sudo EDITOR=vim systemctl edit --force --full dns.slice

[Unit]
Description=System DNS SVC Slice
Documentation=man:systemd.special(7)
DefaultDependencies=no
Before=slices.target

[Slice]
CPUShares=2048

sudo systemctl daemon-reload

sudo EDITOR=vim systemctl edit --force --full stress.service

[Unit]
Description=two cpu usage stress test

[Service]
Type=simple
ExecStart=/usr/bin/stress --cpu 2
Slice=dns.slice

[Install]
WantedBy=multi-user.target

可以通过
systemd-cgtop 查看cgroup状态
systemd-cgls -l
```

## 其他
```
服务清理
systemctl stop [servicename]
systemctl disable [servicename]
rm /etc/systemd/system/[servicename]
rm /etc/systemd/system/[servicename] # and symlinks that might be related
rm /usr/lib/systemd/system/[servicename] 
rm /usr/lib/systemd/system/[servicename] # and symlinks that might be related
systemctl daemon-reload
systemctl reset-failed
```

## ref
* [systemd](https://docs.fedoraproject.org/en-US/quick-docs/systemd-understanding-and-administering/)
* [cgroups](https://wiki.archlinux.org/title/cgroups)
* [cgroups](https://opensource.com/article/20/10/cgroups)