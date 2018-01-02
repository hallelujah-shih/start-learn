set encoding=utf-8
set nu
set tabstop=4
set softtabstop=4
set shiftwidth=4

set ci
set si
set showmatch
set smarttab

filetype plugin indent on
autocmd FileType go set expandtab

function! BuildYCM(info)
    if a:info.status == 'installed' || a:info.force
        " 可以是--all，我这儿主要是C/C++/Python/Go
        !./install.py --clang-completer --gocode-completer
    endif
endfunction

" Specify a directory for plugins
" - For Neovim: ~/.local/share/nvim/plugged
" - 我nvim也是用的vim的目录，便于vim和nvim共用
call plug#begin('~/.local/share/nvim/plugged')
" 编码相关
Plug 'junegunn/vim-easy-align'

Plug 'https://github.com/junegunn/vim-github-dashboard.git'

" 补全相关c-k
Plug 'SirVer/ultisnips' 
Plug 'honza/vim-snippets'

" 左右“属性”栏
Plug 'scrooloose/nerdtree' ", { 'on':  'NERDTreeToggle' }
Plug 'majutsushi/tagbar'

" 编程语言相关
"" golang
Plug 'fatih/vim-go', { 'tag': '*' }
"" nvim
Plug 'nsf/gocode', { 'rtp': 'nvim', 'do': '~/.local/share/nvim/plugged/gocode/nvim/symlink.sh' }
" vim 
" Plug 'nsf/gocode', { 'rtp': 'vim', 'do': '~/.vim/plugged/gocode/vim/symlink.sh' }

"" C/C++
Plug 'vim-scripts/a.vim'
Plug 'vim-scripts/c.vim'
Plug 'octol/vim-cpp-enhanced-highlight'

" markdown
Plug 'godlygeek/tabular'
Plug 'plasticboy/vim-markdown'

" Python
Plug 'Yggdroot/indentLine'
Plug 'tell-k/vim-autopep8'

" 代码补全 
Plug 'Valloric/YouCompleteMe', { 'do': function('BuildYCM') }
Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }

" cscope for nvim
Plug 'mfulz/cscope.nvim'

Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

" neomake linting
Plug 'pearofducks/ansible-vim'
Plug 'neomake/neomake'

call plug#end()

" 代码片段生成，注意冲突
let g:UltiSnipsUsePythonVersion = 2
let g:UltiSnipsExpandTrigger="<c-k>"
let g:UltiSnipsListSnippets="<c-j>"
let g:UltiSnipsJumpForwardTrigger="<c-i>"
let g:UltiSnipsJumpBackwardTrigger="<c-o>"
let g:UltiSnipsEditSplit="vertical"

" 左右“属性”栏的映射
map <C-n> :NERDTreeToggle<CR>
map <C-m> :TagbarToggle <CR>
let g:tagbar_width=30

" ycm代码补全相关
" https://github.com/Valloric/ycmd/blob/master/cpp/ycm/.ycm_extra_conf.py 放入此插件的目录中，加上引用
let g:ycm_global_ycm_extra_conf='~/.local/share/nvim/plugged/YouCompleteMe/.ycm_extra_conf.py'
let g:ycm_use_ultisnips_completer = 1

let g:indentLine_setColors = 0
let g:indentLine_enabled = 1

" let g:cscope_dir = '~/.nvim-cscope'
let g:cscope_map_keys = 1
let g:cscope_update_on_start = 1

" 显示tab
set list
set listchars=tab:>-

" 高亮，nvim好像无效
set hlsearch 
