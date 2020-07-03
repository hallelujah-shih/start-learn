" bug https://github.com/neovim/neovim/wiki/FAQ#nvim-shows-weird-symbols-2-q-when-changing-modes
set guicursor=

set encoding=utf-8
set nu
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab

" 显示tab
set list
set listchars=tab:>-,trail:-

" 高亮，nvim好像无效
set hlsearch

set ci
set si
set showmatch
set smarttab

filetype plugin indent on
autocmd FileType go set expandtab

let g:clang_format#detect_style_file=1
let g:clang_format#auto_format=1

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
Plug 'stamblerre/gocode', { 'rtp': 'nvim', 'do': '~/.local/share/nvim/plugged/gocode/nvim/symlink.sh' }
" vim 
" Plug 'stamblerre/gocode', { 'rtp': 'vim', 'do': '~/.vim/plugged/gocode/vim/symlink.sh' }

" template
Plug 'aperezdc/vim-template'

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

" systemtap
Plug 'nickhutchinson/vim-systemtap'

" 系统配色solarized
Plug 'https://github.com/altercation/vim-colors-solarized'

" fmt
Plug 'rhysd/vim-clang-format'

call plug#end()

" 代码片段生成，注意冲突
if has("python3")
    let g:UltiSnipsUsePythonVersion = 3
else
    let g:UltiSnipsUsePythonVersion = 2
endif
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
let g:ycm_confirm_extra_conf = 0
let g:ycm_global_ycm_extra_conf='~/.ycm_extra_conf.py'
let g:ycm_use_ultisnips_completer = 1
nnoremap <leader>jd :YcmCompleter GoTo<CR>

let g:indentLine_setColors = 0
let g:indentLine_enabled = 1

" let g:cscope_dir = '~/.nvim-cscope'
let g:cscope_map_keys = 1
let g:cscope_update_on_start = 1

" http://cscope.sourceforge.net/cscope_maps.vim
if has("cscope")
	" use both cscope and ctag for 'ctrl-]', ':ta', and 'vim -t'
	set cscopetag
	set csto=0
	if filereadable("cscope.out")
		cs add cscope.out
	elseif $CSCOPE_DB != ""
		cs add $CSCOPE_DB
	endif

	set cscopeverbose

	nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
	nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
	nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
	nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>
	nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>
	nmap <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
	nmap <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
	nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>
endif

" solarized设置
"syntax enable
"if has('gui_running')
"    set background=light
"else
"    set background=dark
"endif
"colorscheme solarized
"let g:solarized_termcolors=256
