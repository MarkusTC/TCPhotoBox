#Mein eigener Code-Versuch

import os
import time
import RPi.GPIO as GPIO
#from leds import Led 
#import led

# Settings #
picture_folder="/var/www/html/images/"
#picture_temp_folder="/pi/Pictures/"
picture_temp_folder="/tmp/"
buzzer_gpio=24
#led_gpio=0

#status_led=led.Led(36);
#status_led.blink_non_stop();
#status_led.blink(0.1);

#Setting Ende #

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def make_photo(make_photo):
    #5 Sekunden warten
    time.sleep(5)
    
    #Event sperren
    #GPIO.remove_event_detect(24)
    
    #Bilder machen
    print("Schnappschuss ...")
    command="gphoto2 --capture-image-and-download --force-overwrite --filename " + picture_temp_folder + "#NR#.jpg"
   
    for i in range(1, 5):
        print("Bild " + str(i) + " wird gemacht...")
        os.system(command.replace("#NR#" ,str(i)))
        
    print ("Foto wird zusammengestellt....")
    tempName=picture_temp_folder + "photobox_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
    newName=picture_folder + "photobox_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
    command="montage " + picture_temp_folder + "1.jpg " + picture_temp_folder+"2.jpg " +picture_temp_folder+"3.jpg "+picture_temp_folder+"4.jpg -geometry +2+2 -resize 3000x2000 -frame 5 " + tempName
    os.system(command)

    
    #Label anbringen
    print ("Label anbringen....")
    command="montage " + tempName + " " + picture_temp_folder + "label.jpg -geometry +1+1 " + newName
    print (command)
    os.system(command)
    print ("Foto wird gedruckt....")

    command="lp -d Canon_CP800 "+newName
    os.system(command)
    print("fertig")

    #Bild umbennen
    #newName="photobox_" + time.strftime('%H%M%S_%d%m%Y') + ".jpg"
    #os.rename("/home/pi/montiert.jpg", "/home/pi/" + newName)

    #from PIL import Image
    #im = Image.open('/home/pi/montiert.jpg')
    #im.show()

    #GPIO.add_event_detect(24, GPIO.RISING, callback=make_photo, bouncetime=300)  


GPIO.add_event_detect(buzzer_gpio, GPIO.RISING, callback=make_photo, bouncetime=300)

try:  
    
    while True:
        time.sleep(1)
        #r=input("Taste für Bild...")
        #make_photo("test")
        
        
except KeyboardInterrupt:
    print("Ende")
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

 

