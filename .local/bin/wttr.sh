#!/usr/bin/env bash
MESSAGE=$(gum style --foreground="10" "Press Enter to continue")
kitty "$SHELL" -c "curl 'ru.wttr.in/Kaliningrad?format=v2d'; \
echo ''
read -rp '$MESSAGE' </dev/tty"
