# install

## gns3 install
```
# ubuntu
sudo add-apt-repository ppa:gns3/ppa
sudo apt update
sudo apt install gns3-gui gns3-server

# fedora
sudo dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf -y install gns3-server gns3-gui dynamips vpcs ubridge xterm
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

## ref
[install-gns3-fedora](https://gerov.eu/posts/how-to-install-gns3-on-fedora/)
