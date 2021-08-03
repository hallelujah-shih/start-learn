# install vim-plug

## for all user
```
sudo mkdir -p /opt/vim/autoload /opt/vim/plugged

# fedora
sudo cp vimrc.local /etc/vimrc.local
# ubuntu
sudo cp vimrc.local /etc/vim/vimrc.local

# install plug
sudo curl -fLo /opt/vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# 这,设置了rtp但是还是不起作用，echo &rtp也是存在的，而:scriptnames是没有的，但是加上下面的链接就好了。。。
ln -s /opt/vim/autoload ~/.vim/autoload

# install plugins
:PlugInstall

#编译ycm
cd /opt/vim/plugged/YouCompleteMe/
# 如果ycm的submodule更新有问题
# git submodule update --init --recursive
# git pull --recurse-sub
python3 install.py --go-completer --clang-completer --system-libclang --clangd-completer

## ubuntu注意
# vim需要高版本
sudo add-apt-repository ppa:jonathonf/vim
sudo apt update
sudo apt install vim
# cmake 需要高版本，如果是ubuntu
sudo snap install cmake --classic
# clang 需要高版本(>=7)
sudo apt install clang-10 libclang-10-dev llvm-10-dev llvm-dev
# ubuntu gcc需要高版本，需支持c++17
sudo apt install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt install g++-10 g++-10-multilib gcc-10 gcc-10-multilib
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 90 --slave /usr/bin/g++ g++ /usr/bin/g++-10 --slave /usr/bin/gcov gcov /usr/bin/gcov-10
```
