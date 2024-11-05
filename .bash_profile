# /etc/skel/.bash_profile

if [[ -f ~/.bashrc ]] ; then
	. ~/.bashrc
fi

# set PATH so it includes user's private */bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
export PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/go/bin" ] ; then
export PATH="$HOME/go/bin:$PATH"
fi

# Ensure XDG_RUNTIME_DIR is set
if test -z "$XDG_RUNTIME_DIR"; then
    export XDG_RUNTIME_DIR=$(mktemp -d /tmp/$(id -u)-runtime-dir.XXX)
fi

# If login is nonroot start session gui, else use console
if shopt -q login_shell; then
    [[ -f ~/.bashrc ]] && source ~/.bashrc
    [[ -t 0 && $(tty) == /dev/tty1 && ! $DISPLAY ]] && exec startx
else
    exit 1 # Somehow this is a non-bash or non-login shell
fi

# For systemD
#[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx
