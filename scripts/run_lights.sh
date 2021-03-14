#!/bin/bash

# Default behavior if no parameters are passed
dev_mode=0
ignore_wemos=0

# Set environment variables for running in development mode and ignoring
# Wemos.
while getopts "dw" OPTION
do
	case "${OPTION}" in
		d) dev_mode=1;;
		w) ignore_wemos=1;;
	esac
done
export dev_mode="$dev_mode";
export ignore_wemos=$ignore_wemos;


cd ~/PiLights/frontend; serve -l 3000 -s build &
cd ~/PiLights/backend; sudo -E flask run --host=192.168.7.99

exit 0
