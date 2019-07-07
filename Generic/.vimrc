
" Configuration file for vim
set modelines=0         " CVE-2007-2438
set nomodeline

" Normally we use vim-extensions. If you want true vi-compatibility
" remove change the following statements
set nocompatible        " Use Vim defaults instead of 100% vi compatibility
set backspace=2         " more powerful backspacing

" Don't write backup file if vim is being called by "crontab -e"
au BufWrite /private/tmp/crontab.* set nowritebackup nobackup
" Don't write backup file if vim is being called by "chpass"
au BufWrite /private/etc/pw.* set nowritebackup nobackup

"Test string for plugins install script

" Plugins
set runtimepath+=~/.vim/boundle/vim-commentary
set runtimepath+=~/.vim/boundle/vim-indent-object
set runtimepath+=~/.vim/boundle/vim-hybrid-master
set runtimepath+=~/.vim/boundle/vim-cpp-enhanced-highlight-master/after

"Cpp Syntax highlight options

let g:cpp_class_scope_highlight = 1
let g:cpp_member_variable_highlight = 1
let g:cpp_class_decl_highlight = 1

"Commentary plugin

autocmd FileType cpp setlocal commentstring=//\ %s
autocmd FileType cc setlocal commentstring=//\ %s
autocmd FileType C setlocal commentstring=//\ %s

" Themes and syntax

set background=dark
colorscheme hybrid

filetype plugin indent on
syntax on

set number relativenumber


let mapleader=" "

"Tab Spaces

set tabstop=3      
set shiftwidth=3    


" Mappings

map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l
map L $
inoremap jj <esc>
vnoremap jkl <esc>
nnoremap ,, ,
nnoremap ,l /

" Latex stuff

autocmd Filetype tex inoremap ,mm <Esc>:w <bar> !pdflatex tesi.tex<ENTER>
autocmd Filetype tex inoremap ,kk <Esc>:w <bar> !pdflatex % && open %:r.pdf<ENTER>
autocmd Filetype tex noremap ,mm <Esc>:w <bar> !pdflatex tesi.tex<ENTER>
autocmd Filetype tex noremap ,kk <Esc>:w <bar> !pdflatex % && open %:r.pdf<ENTER>
autocmd Filetype tex inoremap ,e \begin{equation}<Enter><Enter>\end{equation}<Esc>ki
autocmd Filetype tex inoremap ,emp \emph{}<Esc>i
autocmd Filetype tex inoremap ,bf \textbf{}<Esc>i
autocmd Filetype tex inoremap ,it \textit{}<Esc>i
autocmd Filetype tex inoremap ,ee $$<Esc>i
autocmd Filetype tex inoremap ,lab \label{}<Esc>i
autocmd Filetype tex inoremap ,beg \begin{}<Esc>i
autocmd Filetype tex inoremap ,end \end{}<Esc>i
autocmd Filetype tex inoremap ,sec \section{}<Esc>i
autocmd Filetype tex inoremap ,ssec \subsection{}<Esc>i
autocmd Filetype tex inoremap ,sssec \subsubsection{}<Esc>i
autocmd Filetype tex inoremap ,cha \chapter{}<Esc>i
autocmd Filetype tex inoremap ,fig \begin{figure}[ht]<Enter>\centering<Enter>\makebox[\textwidth][c]{\includegraphics[width=12cm]{Immagini/.jpg}}<Enter>\caption{<Space>}<Enter>\label{<Space>}<Enter>\end{figure}<Esc>3k$5hi
autocmd Filetype tex inoremap ,item \begin{itemize}<Enter>\itemsep-1mm<Enter>\item<Space><Enter>\end{itemize}<Esc>kA
autocmd Filetype tex inoremap ,flalign \begin{flalign}<Enter><Space>&&<Enter>\end{flalign}<Esc>kI
autocmd Filetype tex inoremap ,ffig \begin{figure}[ht]<Enter>\centering<Enter>\begin{subfigure}{.5\textwidth}<Enter><Space>\centering<Enter><Space><Space>\includegraphics[width=1.\linewidth]{Immagini/.jpg}<Enter><Space><Space>\caption{<Space>}<Enter><Space><Space>\label{<Space>}<Enter>\end{subfigure}%<Enter>\begin{subfigure}{.5\textwidth}<Enter><Space><Space>\centering<Enter><Space><Space>\includegraphics[width=1.\linewidth]{Immagini/.jpg}<Enter><Space><Space>\caption{<Space>}<Enter><Space><Space>\label{<Space>}<Enter>\end{subfigure}<Enter>\caption{<Space>}<Enter>\label{<Space>}<Enter>\end{figure}<Esc>12k$4hi
