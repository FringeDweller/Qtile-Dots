# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

export EDITOR='nano'
export VISUAL='nano'
export GTK_THEM=EAdwaita:dark
# My Aliases
#
