#!/usr/bin/python
import RPi.GPIO as GPIO, time, os, subprocess
import random
from shutil import copyfile

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

picture_folder="/var/www/html/images/" #Ordner für die fertige Bilder
picture_temp_folder=""

def showImage(image,old):
  
  print(image + " anzeigen....")
  cmd="display -resize 800X800 -rotate " + str(random.randint(-20,30)) + " " + image
  p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
  
  if old is not None :
    old.kill()
  return p

def deletePrintJobs():
  proc = subprocess.Popen("lpstat",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  #myset=set(proc.stdout)
  #print("Inahlt" + myset)
  for x in proc.stdout : 
    printID=x.split(" ")[0]
    command="cancel " + printID
    gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    #print printID

def enablePrinter():
  command="cupsenable Canon_CP800" 
  gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

deletePrintJobs()

p=None
while True:
  if (GPIO.input(SWITCH)==False):
    snap = 0
    while snap < 4:
      print("pose!")
      if p is None:            
        p=showImage("pose.jpg",None)
      else:
        p=showImage("pose.jpg",p)

      #GPIO.output(BUTTON_LED, False)
      #GPIO.output(POSE_LED, True)
      #time.sleep(1.5)
      #for i in range(5):
      #  GPIO.output(POSE_LED, False)
      #  time.sleep(0.4)
      #  GPIO.output(POSE_LED, True)
      #  time.sleep(0.4)
      #for i in range(5):
      #  GPIO.output(POSE_LED, False)
      #  time.sleep(0.1)
      #  GPIO.output(POSE_LED, True)
      #  time.sleep(0.1)
      #GPIO.output(POSE_LED, False)

      time.sleep(8)
      p.kill()
      print("SNAP")

      command="gphoto2 --capture-image-and-download --force-overwrite --filename " + picture_temp_folder + "#NR#.jpg"
      command=command.replace("#NR#" ,str(snap+1))
      
      gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
      
      #Bild anzeigen
      p=showImage(picture_temp_folder + "#NR#.jpg".replace("#NR#" ,str(snap+1)),p)
      
      print(gpout)
      #if "ERROR" not in gpout: 
      snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(15)

    print("please wait while your photos print...")
    #GPIO.output(PRINT_LED, True)
    
    # build image and send to printer
    subprocess.call("bash tc_montage.sh", shell=True)
    
    dest=picture_folder + "photobox_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
    src="polaroid_overlap.jpg"
    
    #Bild anzeigen
    p.kill
    p=showImage(src,p)

    copyfile(src, dest)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time

    command="lp -d Canon_CP800 "+dest
    subprocess.call(command, shell=True)

    time.sleep(1)
    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
