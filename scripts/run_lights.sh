#!/bin/bash

# Default behavior if no parameters are passed
dev_mode=0
ignore_wemos=0

# Set environment variables for running in development mode and ignoring
# Wemos.
while getopts "dw" OPTION
do
	case "${OPTION}" in
		d) dev_mode=1; 
		echo "Starting in development mode. Functionality will be limited for compatibility.";;
		w) ignore_wemos=1;
		echo "Skipping Wemo discovery.";;
	esac
done
export dev_mode="$dev_mode";
export ignore_wemos=$ignore_wemos;

# Spin up frontend and backend
cd ~/PiLights/frontend; serve -l 3000 -s build &
cd ~/PiLights/backend; sudo -E flask run --host=192.168.7.99

# Kill the frontend and backend if the terminal is exited
trap 'kill 0 & echo "Killing all processes..."' EXIT
