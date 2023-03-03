# hello
```
示例
```

## 编写helm chart
### NodePort
```
helm create hello-nodeport

修改 Chart.yaml:
    appVersion 为: v1
修改 values.yaml:
    service.type 为: NodePort
    image.repository 为: hello-app
修改 templates/deployment.yaml:
    spec.template.spec.containers
        ports下面将服务暴露containerPort: 8080
```

### ClusterIP + ingress
```
INGRESS_IP=`minikube ip`
此处假设为: 192.168.49.2

helm create hello-clusterip

修改 Chart.yaml:
    name: hello-app
    appVersion 为: v1

修改 values.yaml:
    image.repository 为: hello-app
    ingress.enabled 为: true
    ingress.hosts.host 为: 192.168.49.2.nip.io // nip.io是rsp指定ip的dns服务

修改 templates/deployment.yaml:
    spec.template.spec.containers
        ports下面将服务暴露containerPort: 8080

修改 templates/service.yaml:
    spec.ports.port.targetPort 为 8080
```

### LoadBalancer
```
helm create hello-loadbalancer

修改 Chart.yaml:
    name: hello-app
    appVersion 为: v1

修改 values.yaml:
    image.repository 为: hello-app
    ingress.enabled 为: true
    ingress.hosts.host 为: hello.10.8.160.102.nip.io
    service.type 为 LoadBalancer

修改 templates/deployment.yaml:
    spec.template.spec.containers
        ports下面将服务暴露containerPort: 8080

修改 templates/service.yaml:
    spec.ports.port.targetPort 为 8080

* 为了全程模拟
```

## 构建docker
```
// hello-app是chart.name v1是chart.appVersion
## 方法1
eval $(minikube docker-env)
docker build . -t hello-app:v1 

## 方法2
docker build . -t hello-app:v1
docker save hello-app:v1 -o hello-app.tar
minikube cp hello-app.tar /tmp/hello-app.tar
minikube ssh "docker load -i /tmp/hello-app.tar"
```

## 部署
```
helm install hello-app ./hello-app

# debug 输出渲染
helm install hello-app ./hello-app --dry-run --debug

# list
helm ls

# uninstall
helm uninstall hello-app

# upgrade
helm upgrade hello-app ./hello-app
```
