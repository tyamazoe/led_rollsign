#!/bin/bash

# Run forever [-l 0] with a 1 second delay [-d 1.0] between images with adafruit-hat
# sudo python3 ./python/imagefolder.py -f ./image -m adafruit-hat -b 60 -d 1.0 -l 0

# Run once [-l 1] with a 1.5 second delay [-d 1.5] between images with regular GPIO
sudo python3 ./python/imagefolder.py -f ./image -m regular -b 60 -d 1.5 -l 1 

