#!/bin/bash
gentoo-pipewire-launcher &
/usr/libexec/polkit-kde-authentication-agent-1 &
picom --daemon &
waypaper --restore &
nm-applet &
blueman-applet &
