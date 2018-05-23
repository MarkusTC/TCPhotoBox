#!/usr/bin/python

from PIL import Image
import RPi.GPIO as GPIO, time, os, subprocess

cmd="display -resize 1000X800 -rotate -25 /home/pi/share/toPhoto/Jil_Portrait.jpg"
p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
time.sleep(10)
p.kill()

print("fertig")
