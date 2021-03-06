#Some suggestions for frequently used commands:
alias cd..='cd ..'
alias cp='cp -i'
alias d='ls'
alias df='df -h -x supermount'
alias du='du -h'
alias egrep='egrep --color'
alias fgrep='fgrep --color'
alias grep='grep --color'
alias l='ls'
alias la='ls -a'
alias ll='ls -l'
alias ls='ls -F --color=auto'
alias lsd='ls -d */'
alias md='mkdir'
alias mv='mv -i'
alias p='cd -'
alias rd='rmdir'
alias rm='rm -i' 
alias rm='rm -i' 
alias docs='cd /home/mmelcot/Development/ASB/WP_3000.V1'
alias sl='ls'
alias openf='xdg-open'
alias t='tree'
alias env='env | sort'
# file find:
alias f="find . -type f -iname "
# All files in dir (recursive)
alias ff="find . -type f"
# All dir in dir (recursive)
alias fd="find . -type d"
alias watch="watch -n 0.5"
alias o='xdg-open'
alias psl='sudo git push origin master'
alias vi='vim'

# Change directory aliases
alias home='cd ~'
alias cd..='cd ..'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# Remove a directory and all files
alias rmd='/bin/rm  --recursive --force --verbose '

# "que pasa":
alias qp="ps auxwww | more"

# SMOS L1OP
alias scenar="cd /mnt/eos-share/apps/SMOS_L1OP"
alias catsmos="pygmentize -l smos"
alias cats="catsmos"
alias mkvenv="virtualenv venv"
alias rvenv="source venv/bin/activate"


