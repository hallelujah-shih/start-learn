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

## 注意，若发现Fedora的安装，docker不能启动，可能就需要手动安装gns3-server和gns3-gui
mkdir ~/gns3
cd ~/gns3

git clone https://github.com/GNS3/gns3-server.git
cd gns3-server
sudo pip3 install -r requirements.txt
sudo python3 setup.py install

git clone https://github.com/GNS3/gns3-gui.git
cd gns3-gui
sudo pip3 install -r requirements.txt
sudo python3 setup.py install
sudo cp resources/linux/applications/gns3.desktop /usr/share/applications/
sudo cp -R resources/linux/icons/hicolor/ /usr/share/icons/


// git clone https://github.com/GNS3/vpcs.git
// cd vpcs
// ./mk.sh
// sudo cp vpcs /usr/local/bin/vpcs

// git clone https://github.com/GNS3/dynamips.git
// cd dynamips
// mkdir build 
// cd build/
// cmake ..
// make
// sudo make install

// git clone https://github.com/GNS3/ubridge.git
// cd ubridge
// make
// sudo make install
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
[install-gns3-on-centos](https://techviewleo.com/how-to-install-gns3-on-centos-rhel-linux/)
