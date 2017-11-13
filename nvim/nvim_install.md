# nvim
```
另一个vim
```

## nvim install
```
neovim安装完成后，需执行
    > pip install neovim
```
### CentOS 7/RHEL 7
```sh
yum -y install epel-release
curl -o /etc/yum.repos.d/dperson-neovim-epel-7.repo https://copr.fedorainfracloud.org/coprs/dperson/neovim/repo/epel-7/dperson-neovim-epel-7.repo 
yum -y install neovim

```

### Ubuntu
```
依赖项安装：
> sudo apt-get install python-dev python-pip python3-dev python3-pip

14.04及其以上
> sudo apt-get install software-properties-common
更老版本的
> sudo apt-get install python-software-properties

安装
> sudo add-apt-repository ppa:neovim-ppa/stable
> sudo apt-get update
> sudo apt-get install neovim

"永久性工事"
sudo update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60
sudo update-alternatives --config vi
sudo update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60
sudo update-alternatives --config vim
sudo update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
sudo update-alternatives --config editor
```

##配置nvim插件（C/C++/Python/Go程序猿版）
```
所有插件通过vim-plug插件来管理

安装vim-plug插件
> curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
若用于vim执行下面的命令
> curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
>     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

### 个人插件
```vim
" 路径 nvim(~/.config/nvim/init.vim) vim(~/.vimrc)
set encoding=utf-8
set nu
set tabstop=4
set softtabstop=4
set shiftwidth=4

set ci
set si
set hls 
set showmatch
set smarttab
autocmd FileType go set expandtab

filetype plugin indent on

" Specify a directory for plugins
" - For Neovim: ~/.local/share/nvim/plugged
" - 我nvim也是用的vim的目录，便于vim和nvim共用
call plug#begin('~/.vim/plugged')

Plug 'junegunn/vim-easy-align'

Plug 'https://github.com/junegunn/vim-github-dashboard.git'

Plug 'SirVer/ultisnips' 
" Plug 'honza/vim-snippets'

Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }

Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }

Plug 'fatih/vim-go', { 'tag': '*' }

Plug 'nsf/gocode', { 'tag': 'v.20150303', 'rtp': 'vim' }

Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

Plug 'majutsushi/tagbar'

function! BuildYCM(info)
    if a:info.status == 'installed' || a:info.force
		" 可以是--all，我这儿主要是C/C++/Python/Go
		!./install.py --clang-completer --gocode-completer
	endif
endfunction
Plug 'Valloric/YouCompleteMe', { 'do': function('BuildYCM') }

Plug 'godlygeek/tabular'			            

Plug 'plasticboy/vim-markdown'

Plug 'vim-scripts/a.vim'
Plug 'vim-scripts/c.vim'

" Unmanaged plugin (manually installed and updated)
Plug '~/my-prototype-plugin'

call plug#end()


let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

map <C-n> :NERDTreeToggle<CR>
nmap <C-m> :TagbarToggle <cr>
let g:tagbar_width=30

" https://github.com/Valloric/ycmd/blob/master/cpp/ycm/.ycm_extra_conf.py 放入此插件的目录中，加上引用
" C/c++的头文件目录还需要加入到.ycm_extra_conf.py中
let g:ycm_global_ycm_extra_conf='~/.vim/plugged/YouCompleteMe/.ycm_extra_conf.py'

```

### 安装插件
```
打开nvim并执行
:PlugInstall
```
#### YouCompleteMe说明
```
若中途失败，则需要到plugged/YouCompleteMe目录下执行依赖项的仓库重新拉取并编译
> git submodule update --init --recursive
编译，我这儿只要C家族的和Go语言
> ./install.py --clang-completer --gocode-completer
```
#### vim-go说明 
```
自己设置好go的环境变量后，需要在nvim中执行
:GoInstallBinaries
需要注意的是国内网络环境“复杂多变”，需要将环境变量设置好
> export https_proxy=http://192.168.1.1:8118/
> export http_proxy=http://192.168.1.1:8118/

```

## reference
    [neovim install wiki](https://github.com/neovim/neovim/wiki/Installing-Neovim)
    [vim-plug](https://github.com/junegunn/vim-plug)
