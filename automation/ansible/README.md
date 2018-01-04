# asnible
```
一个简单的自动化运维工具
```

## 安装
```bash
# Fedora 27
sudo dnf -y install ansible
```
## 杂项说明
```
多用户下，使用自己的配置问题
加载顺序，我是使用的$HOME/.ansible.cfg作为全局配置
* ANSIBLE_CONFIG (an environment variable)
* ansible.cfg (in the current directory)
* .ansible.cfg (in the home directory)
* /etc/ansible/ansible.cfg

关闭SSH key的host checking（编辑ansible.conf的host_key_checking）
host_key_checking = False

SSH key输入密码的问题（使用ssh-agent + ssh-add解决）
方便使用ssh-agent生成的环境变量，于每个shell自动运行
$ echo 'eval $(ssh-agent)' >> ~/.bash_profile
$ ssh-add my_private_key_path
```
