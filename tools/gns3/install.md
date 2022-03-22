# install

## gns3 install
```
sudo add-apt-repository ppa:gns3/ppa
sudo apt update
sudo apt install gns3-gui gns3-server
```

## docker install
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"

sudo apt update
sudo apt install docker-ce
```
### 添加组
```
for item in ubridge libvirt kvm wireshark docker; do sudo usermod -aG $item `whoami`; done
```

