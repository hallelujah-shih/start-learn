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

filetype plugin indent on
autocmd FileType go set expandtab

" Specify a directory for plugins
" - For Neovim: ~/.local/share/nvim/plugged
" - 我nvim也是用的vim的目录，便于vim和nvim共用
call plug#begin('~/.local/share/nvim/plugged')

Plug 'junegunn/vim-easy-align'

Plug 'https://github.com/junegunn/vim-github-dashboard.git'

Plug 'SirVer/ultisnips' 
" 会和YouCompleteMe冲突
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

Plug 'Yggdroot/indentLine'
Plug 'tell-k/vim-autopep8'

" C++高亮
Plug 'octol/vim-cpp-enhanced-highlight'

call plug#end()

let g:UltiSnipsUsePythonVersion = 2
" 
let g:UltiSnipsExpandTrigger="<C-j>"
let g:UltiSnipsJumpForwardTrigger="<C-b>"
let g:UltiSnipsJumpBackwardTrigger="<C-z>"
let g:UltiSnipsEditSplit="vertical"

map <C-n> :NERDTreeToggle<CR>
map <C-m> :TagbarToggle <CR>
let g:tagbar_width=30

" https://github.com/Valloric/ycmd/blob/master/cpp/ycm/.ycm_extra_conf.py 放入此插件的目录中，加上引用
let g:ycm_global_ycm_extra_conf='~/.local/share/nvim/plugged/YouCompleteMe/.ycm_extra_conf.py'
let g:ycm_use_ultisnips_completer = 1

let g:indentLine_setColors = 0
let g:indentLine_enabled = 1
