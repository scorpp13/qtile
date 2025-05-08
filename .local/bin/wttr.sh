#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NONE='\033[0m'

kitty "$SHELL" -c "curl 'ru.wttr.in/Kaliningrad?format=v2d'; \
echo -e '$GREEN'
read -rp 'Press Enter to continue' </dev/tty"
