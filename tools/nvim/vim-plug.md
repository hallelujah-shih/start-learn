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
python3 install.py --go-completer --clang-completer --system-libclang --clangd-completer
```
