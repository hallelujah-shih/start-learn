# minikube

## install
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl
```

## autocompletion
```
echo 'source <(kubectl completion bash)' >>~/.bashrc
echo 'source <(minikube completion bash)' >>~/.bashrc
```
## start
```
minikube start --image-mirror-country='cn'
```


## minikube的registry-mirrors修改
```
文件：~/.minikube/machines/minikube/config.json

"RegistryMirror": ["https://docker.mirrors.ustc.edu.cn/"],
```

## usage
```
kubectl basic usage:
CRUD cmds
create deployment           kubectl create deployment [name] --image=image [--dry-run] [options]
edit deployment             kubectl edit deployment [name]
delete deployment           kubectl delete deployment [name]

Status of K8S components
kubectl get nodes|pod|services|replicaset|deployment

Debugging pods
Log to console              kubectl logs [pod name]
get interactive terminal    kubectl exec -it [pod name] -- /bin/bash
get info about pod          kubectl describe pod [pod name]

Use configuration file for CRUD
Apply a cfg file            kubectl apply -f [file name]
Delete with cfg file        kubectl delete -f [file name]

```
## k8s关键构成介绍
### k8s主要组件
```
pod:
service:
ingress:
volumes:
comfigmap:
secrets:
deployment: for state-less apps
statefulset: for state-full apps or databases
```

### k8s的worker节点的3个程序
```
kubelet:
kube proxy:
container runtime:
```
### k8s的master节点的4个程序
```
api server:
scheduler:
controller manager:
etcd:
```
## REF
[kubectl basic cmd](https://www.youtube.com/watch?v=azuwXALfyRg)
