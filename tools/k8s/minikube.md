# minikube
```
本地测试环境
```

## install
```
安装相关
```

### minikube
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### kubectl
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl
```

### helm
```
curl -L https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz | sudo tar -xzv --strip-components=1 -C /usr/local/bin

helm repo add bitnami https://charts.bitnami.com/bitnami
```

## start
```
# 初始化
minikube start --image-mirror-country='cn' --kubernetes-version=1.23.0 --memory 10240

# 替换镜像
sed -i 's|.*RegistryMirror.*|"RegistryMirror": ["https://docker.mirrors.ustc.edu.cn/", "https://registry.cn-hangzhou.aliyuncs.com", "http://hub-mirror.c.163.com", "https://registry.docker-cn.com"],|g' $HOME/.minikube/machines/minikube/config.json

# 重启
minikube stop
minikube start

# 查看镜像信息
minikube ssh "docker info"
```

### 开启常用插件
```
minikube addons enable ingress
minikube addons enable dashboard
minikube addons enable metrics-server
```

### 开发、部署简单一条龙(不带ingress)
```
# dashboard
minikube dashboard --url

# ip
minikube ip

# 创建服务
参见 hello/README.md

# 部署
参见 hello/README.md

# 查看pods
kubectl get pods

# 查看deployments
kubectl get deployments

# 暴露IP
1. 获取url
    minikube service hello-app --url
```

### 开发、部署简单一条龙(ingress)
```
# 创建服务
参见 hello/README.md

# 部署
helm install hello-app ./hello-app-ingress

# 查看pods
kubectl get pods

# 查看deployments
kubectl get deployments

# 访问
curl 192.168.49.2.nip.io
```

### 排查问题
```
# 查看状态
kubectl get xxx

# 查看描述
kubectl describe xxx

# 查看日志
kubectl logs xxx

# 进入容器看看
kubectl exec -it -n <namespace> instance -- 要执行的cmd，如bash

# 终极杀招
## 创建一个curl容器，并运行
kubectl run -it --rm test --image=curlimages/curl --restart=Never -- /bin/sh
## 根据自己需要瞎搞（测试）
curl xxxx
## gdb
minikube ssh
docker ps |grep "xxxx"
docker exec -it --user=0 --privileged container_id bash
```

### 查看配置
```
# 查看ingress的
kubectl describe ingress hello-app
# 查看service的
kubectl describe service hello-app
# 查看pod的
kubectl describe pod hello-app
```

## 部署gitlab

### 克隆gitlab chart repo
```
git clone https://gitlab.com/gitlab-org/charts/gitlab.git
cd gitlab
```

### 部署
```
# 使用推荐设置部署
helm dependency update
helm upgrade --install gitlab . \
  --timeout 600s \
  --set global.hosts.domain=$(minikube ip).nip.io \
  --set global.hosts.externalIP=$(minikube ip) \
  -f https://gitlab.com/gitlab-org/charts/gitlab/raw/master/examples/values-minikube.yaml

# 使用最小设置部署
helm dependency update
helm upgrade --install gitlab . \
  --timeout 600s \
  --set global.hosts.domain=$(minikube ip).nip.io \
  --set global.hosts.externalIP=$(minikube ip) \
  -f https://gitlab.com/gitlab-org/charts/gitlab/raw/master/examples/values-minikube-minimum.yaml
```

## REF
* [troubleshooting](https://kubernetes.github.io/ingress-nginx/troubleshooting/)
* [Setup gitlab on minikube using helm3](https://gist.github.com/nirbhabbarat/8fe32ccaaacc782272c9f49a753e97b4)
* [Developing for Kubernetes with minikube](https://docs.gitlab.com/charts/development/minikube/)
* [nip.io](https://nip.io/)