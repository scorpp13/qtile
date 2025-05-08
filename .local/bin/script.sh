#!/usr/bin/env bash

option1="  Rofi themes"
option2="  Convert to gif"
option3="  Convert to jpg"
option4="  Merge images"
option5="  Archive extractor"
option6="  Font search"

options="$option1\n$option2\n$option3\n$option4\n$option5\n$option6"

choice=$(echo -e "$options" | rofi -dmenu -replace -config ~/.config/rofi/script.rasi -i -no-show-icons -l 6 -width 30) 

case $choice in
	"$option1")
		kitty "$SHELL" -c "rtheme.sh" ;;
	"$option2")
		kitty "$SHELL" -c "convert-to-gif.sh" ;;
	"$option3")
		kitty "$SHELL" -c "convert-to-jpg.sh" ;;
	"$option4")
		kitty "$SHELL" -c "merge_img.sh" ;;
	"$option5")
		kitty "$SHELL" -c "extract.sh" ;;
	"$option6")
		kitty "$SHELL" -c "fontsearch.sh" ;;
esac
