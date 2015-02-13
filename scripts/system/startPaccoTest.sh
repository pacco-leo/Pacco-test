#!/bin/sh
#title           :startMidori
#description     : 
#author          :paccotest  
#date            :20140702
#version         :0.1
#usage           : 
#notes           : 
#bash_version    : 
#==============================================================================

export PACCO_DIR="/home/pi/PaccoTest/"

xset -dpms     # disable DPMS (Energy Star) features.
xset s off       # disable screen saver
xset s noblank # don't blank the video device

python $PACCO_DIR/app/manage.py runserver # start Django server

unclutter &
matchbox-window-manager &

# Choose which page to run, depending if connection to internet is on or off
wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
    echo "Online"
    #REPLACE THIS BY THE UPLOAD PAGE
    # epiphany-browser http://www.playr.biz/23612/15122
	#sleep 2s # give it time to start
	#echo key F11 | xte # simulate pressing the full screen key
    chromium --kiosk http://localhost:8000/paccotest/uploadToServer/
else
    echo "Offline"
    chromium --kiosk http://localhost:8000/paccotest/opening/
fi
