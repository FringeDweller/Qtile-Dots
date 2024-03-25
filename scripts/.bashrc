# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

export EDITOR='nvim'
export VISUAL='nvim'
export GTK_THEM=EAdwaita:dark
# My Aliases
#
alias nv=nvim