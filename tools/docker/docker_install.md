# docker 安装
```
安装记录
```

## ubuntu >= 18.04 LTS
```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# add official GPG KEY:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# add source
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install docker engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

```

## Manage Docker as a non-root user
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

## ref
	https://docs.docker.com/engine/install/ubuntu/
	https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
