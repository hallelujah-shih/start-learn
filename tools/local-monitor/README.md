# 构建本地监控环境(测试环境使用)

## influxdb-grafana
```
使用仓库地址：https://github.com/nicolargo/docker-influxdb-grafana.git

clone到本地:
    git clone https://github.com/nicolargo/docker-influxdb-grafana.git

    根据需求修改：docker-compose.yml
        特别是 volumes
        删除 telegraf

    注释掉文件：env.grafana，主要是国内网络的问题

    修改文件 run.sh 并确保volumes的目录与 docker-compose的是匹配的

    运行：
    bash run.sh

    打开 http://localhost:3000/
    添加数据源： influxdb的时候，URL：http://influxdb:8086， DATABASE: telegraf  （这个是示例的telegraf的名字，根据自己需要添加，与telegraf的配置文件匹配即可）

    influxdb数据源：
    Network Interface Stats: https://grafana.com/grafana/dashboards/10488
    Telegraf Host Metrics: https://grafana.com/grafana/dashboards/1443
    Telegraf system dashboard: https://grafana.com/grafana/dashboards/928

    prom数据源:
    Alerts Linux nodes: https://grafana.com/grafana/dashboards/5984
    Linux Hosts Metrics: https://grafana.com/grafana/dashboards/10180


```

## prometheus
```
运行docker: docker run -p 9090:9090 prom/prometheus
```

## telegraf
```
下载telegraf包
修改 telegraf.conf配置文件, 替换outputs.influxdb的urls
运行 telegraf -config telegraf.conf
```

## ebpf_exporter
```
编译二进制
cd $(mktemp -d)
GOPATH=$(pwd) go get -v github.com/cloudflare/ebpf_exporter/...

```

## ref
    https://github.com/iovisor/bcc/blob/master/INSTALL.md
    https://github.com/cloudflare/ebpf_exporter
    https://andrewhowdencom.medium.com/adventures-with-ebpf-and-prometheus-6a59dd170b26
