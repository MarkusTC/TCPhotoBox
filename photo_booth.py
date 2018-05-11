#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN,pull_up_down=GPIO.PUD_UP)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

picture_folder="/var/www/html/images/"
picture_temp_folder="/tmp/"

while True:
  #print("start")
  if (GPIO.input(SWITCH)==False):
    snap = 0
    while snap < 4:
      print("pose!")
      GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      print("SNAP")

      command="gphoto2 --capture-image-and-download --force-overwrite --filename " + picture_temp_folder + "#NR#.jpg"
      #command.replace("#NR#" ,snap)
      
      #gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
      #print(gpout)
      #if "ERROR" not in gpout: 
      snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(0.5)
    print("please wait while your photos print...")
    GPIO.output(PRINT_LED, True)
    # build image and send to printer
    #subprocess.call("montage", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    time.sleep(1)
    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
