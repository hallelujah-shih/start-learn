# CPU limit
## cgroup-v1
```
sudo cgcreate -g cpu:/cpulowusage
# sudo cgcreate -t $USER:$USER -a $USER:$USER -g cpu:/cpulowusage
// 设置单CPU 20% 限制
sudo cgset -r cpu.cfs_period_us=100000 cpulowusage
sudo cgset -r cpu.cfs_quota_us=20000 cpulowusage
sudo cgset -r cpu.shares=256 cpulowusage
sudo cgget -g cpu:cpulowusage

// 执行 1
sudo cgexec -g cpu:cpulowusage python hello0.py
// 执行带nice
cgexec -g cpu:cpulowusage nice -n 19 python3 main.py --config settings.yaml.test
```
## cgroup-v2
```
sudo cgcreate -t $USER:$USER -a $USER:$USER -g cpu:/cpulowusage
cgset -r cpu.weight=200 cpulowusage
cgset -r cpu.weight.nice=19 cpulowusage
cgset -r cpu.max="max 500" cpulowusage
```

## ref
[Limiting Process Resource](https://www.baeldung.com/linux/limit-resource-consumption)
[How to Limit CPU Usage of a Process on Linux](https://linuxhint.com/limit_cpu_usage_process_linux/)
[cpu-limit](https://www.kernel.org/doc/html/latest/scheduler/sched-bwc.html)
[cgroup-v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)
[cgroup-v2](https://facebookmicrosites.github.io/cgroup2/docs/cpu-controller.html)
