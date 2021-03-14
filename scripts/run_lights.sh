#!/bin/bash

cd ~/PiLights/frontend; serve -l 3000 -s build & 
cd ~/PiLights/backend; sudo flask run --host=192.168.7.99
