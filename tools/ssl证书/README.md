# CA

## 根证书安装为可信

### fedora
```
sudo cp root.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

### ubuntu
```
sudo apt-get install -y ca-certificates
sudo cp root.pem /usr/local/share/ca-certificates
sudo update-ca-certificates
```