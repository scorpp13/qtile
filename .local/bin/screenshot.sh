#!/bin/bash

option1="  Entire Desktop"
option2="  Flameshot GUI"
option3="  Configure"
option4="  Wallpaper"

options="$option1\n$option2\n$option3\n$option4"

choice=$(echo -e "$options" | rofi -dmenu -replace -config ~/.config/rofi/screenshot.rasi -i -no-show-icons -l 4 -width 30) 

case $choice in
	$option1)
		sleep 1 && flameshot full ;;
	$option2)
		flameshot gui ;;
	$option3)
		flameshot config ;;
	$option4)
		waypaper ;;
esac
