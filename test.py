#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    
    #print("hello")
    if (GPIO.input(SWITCH)==False):
        print("SNAP")
        time.sleep(0.5)

