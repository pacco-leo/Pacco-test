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

#!/bin/sh
while true; do

	# Clean up previously running apps, gracefully at first then harshly
	killall -TERM chromium 2>/dev/null;
	killall -TERM matchbox-window-manager 2>/dev/null;
	sleep 2;
	killall -9 chromium 2>/dev/null;
	killall -9 matchbox-window-manager 2>/dev/null;

	# Clean out existing profile information
	rm -rf /home/pi/.cache;
	rm -rf /home/pi/.config;
	rm -rf /home/pi/.pki;

	# Generate the bare minimum to keep Chromium happy!
	mkdir -p /home/pi/.config/chromium/Default
	sqlite3 /home/pi/.config/chromium/Default/Web\ Data "CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR); INSERT INTO meta VALUES('version','46'); CREATE TABLE keywords (foo INTEGER);";

	# Disable DPMS / Screen blanking
	xset -dpms
	xset s off

	# Reset the framebuffer's colour-depth
	fbset -depth $( cat /sys/module/*fb*/parameters/fbdepth );

	# Hide the cursor (move it to the bottom-right, comment out if you want mouse interaction)
	xwit -root -warp $( cat /sys/module/*fb*/parameters/fbwidth ) $( cat /sys/module/*fb*/parameters/fbheight )

	# Start the window manager (remove "-use_cursor no" if you actually want mouse interaction)
	matchbox-window-manager -use_titlebar no -use_cursor no &

	# Start the App	
	export PACCO_DIR="/home/pi/PaccoTest/"
	python $PACCO_DIR/app/manage.py runserver & # start Django server

	# Start the browser (See http://peter.sh/experiments/chromium-command-line-switches/)
	## Choose which page to run, depending if connection to internet is on or off
	wget -q --tries=10 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
	    echo "Online"
	    #REPLACE THIS BY THE UPLOAD PAGE
	    # epiphany-browser http://www.playr.biz/23612/15122
		#sleep 2s # give it time to start
		#echo key F11 | xte # simulate pressing the full screen key
	    sleep 10
	    chromium --app=http://localhost:8000/paccotest/uploadToServer/
	else
	    echo "Offline"
	    sleep 10
	    chromium --app=http://localhost:8000/paccotest/opening/ --user-data-dir
	fi
	
	
done;
