#!/bin/sh
gentoo-pipewire-launcher &
/usr/libexec/polkit-gnome-authentication-agent-1 &
picom --daemon &
waypaper --restore &
#~/.fehbg &
nm-applet &
