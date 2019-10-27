# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples
# PS1="\[\e[92m\]Fra#Psi:\w>\[\e[m\]"
PS1="\[\e[38;5;82m\]Fra#Psi:\w>\[\e[m\]"

bind TAB:menu-complete

alias kdev='KDevelop-5.3.2-x86_64.AppImage &'

fanblast(){ sudo fanblast.sh $1; }

cpu(){ echo ; echo "CPU Frequency:" ; echo ; cat /proc/cpuinfo | grep MHz ; echo "" ; echo "Temperature:"; echo ; sensors | grep "Core\|side" ; }

batt(){ echo ; upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "energy-full|energy-rate|time to|percentage|capacity"; echo; }

alias watch='watch '

alias l='ls -lah'

bat(){ echo "##############################";	
       echo -n "# Full Battery Design: " ; sudo tlp-stat -b | grep "charge_full_" | awk '{ printf "%5s #",$3}' ; echo ;
       echo -n  "# Full Battery: " ; sudo tlp-stat -b | grep -w "charge_full" | awk '{printf "%12s #", $3}' ; echo ;
       echo -n  "# Remaining Battery: " ;sudo tlp-stat -b | grep charge_now | awk '{printf "%7s #", $3}' ; echo ;
       stato=$(sudo tlp-stat -b | grep -w "status" | awk '{print $3}') ;
       if [ "$stato" = "Discharging" ]; then 
	       echo -n  "# Power Drain: " ; sudo tlp-stat -b | grep current_now | awk  '{ printf "\033[31m%13s\033[0m #", $3 }' ; echo;
       elif [ "$stato" = "Charging" ]; then 
	       echo -n  "# Power Charge: " ; sudo tlp-stat -b | grep current_now | awk  '{ printf "\033[37m%12s\033[0m #", $3 }' ; echo ; 
       fi ;
       echo "##############################"; }

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
#HISTSIZE=1000
#HISTFILESIZE=2000

# Eternal bash history.
# ---------------------
# Undocumented feature which sets the size to "unlimited".
# http://stackoverflow.com/questions/9457233/unlimited-bash-history
export HISTFILESIZE=
export HISTSIZE=
export HISTTIMEFORMAT="[%F %T] "
# Change the file location because certain bash sessions truncate .bash_history file upon close.
# http://superuser.com/questions/575479/bash-history-truncated-to-500-lines-on-each-login
#export HISTFILE=~/.bash_eternal_history
# Force prompt to write history after every command.
# http://superuser.com/questions/20900/bash-history-loss
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"


# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
#[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

#if [ "$color_prompt" = yes ]; then
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
#else
#    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
#fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    #alias grep='grep --color=auto'
    #alias fgrep='fgrep --color=auto'
    #alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
alias NumericPlatform='export NUPLAT=/home/frapsi/Software/NumericPlatform && cd $NUPLAT && source plat_conf.sh && cd - '

