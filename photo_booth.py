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

picture_folder="images/" #Ordner für die fertige Bilder
picture_folder_web="/var/www/html/images/" #Web-Ordner für die fertige Bilder
picture_temp_folder="tmp/"

printerid="Canon_CP800"

def showImage(image,old):
  
  print(image + " anzeigen....")
  #cmd="display -resize 800X800 -rotate " + str(random.randint(-20,30)) + " " + image
  cmd="display -resize 1000X800 " + image
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

def minimizeImages(image):
  command="mogrify -resize 864X648 " + image
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
     

      time.sleep(8)
      p.kill()

      #Foto machen
      print("SNAP")
      src=picture_temp_folder + "#NR#.jpg".replace("#NR#" ,str(snap+1)) 
      command="gphoto2 --capture-image-and-download --force-overwrite --filename " + src
      command=command.replace("#NR#" ,str(snap+1))
      gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

      #... Original-Foto im Foto-Ordner sichern
      dest=picture_folder + "#NR#_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
      dest=dest.replace("#NR#" ,str(snap+1))
      
      copyfile(src, dest)

      #... Bild verkleinern
      minimizeImages(src)
      
      #Bild anzeigen
      p=showImage(src,p)
      
      print(gpout)
      #if "ERROR" not in gpout: 
      snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(15)
    
    # build image and send to printer
    print("please wait while your photos print...")
    subprocess.call("bash tc_montage.sh", shell=True)
    
    src="polaroid_overlap.jpg"
    
    #Bild anzeigen
    p.kill
    p=showImage(src,p)
    #Bild zum Webserver kopieren
    dest=picture_folder_web + "photobox_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
    copyfile(src, dest)

    #Bild drucken
    enablePrinter()
    command="lp -d Canon_CP800 "+dest
    subprocess.call(command, shell=True)

    time.sleep(1)
    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
