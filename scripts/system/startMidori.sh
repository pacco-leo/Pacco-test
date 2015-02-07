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

export PACCO_DIR = "/home/pi/PaccoTest/"

xset -dpms     # disable DPMS (Energy Star) features.
xset s off       # disable screen saver
xset s noblank # don't blank the video device

python $PACCO_DIR/apps/manage.py runserver # start Django server

unclutter &
matchbox-window-manager &

midori -e Fullscreen -a http://localhost:8000/paccotest/ouverture/
