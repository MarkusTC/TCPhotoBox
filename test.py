import printer, time


##### Einstellungen ####
picture_folder="images/" #Ordner für die fertige Bilder
picture_folder_web="/var/www/html/images/" #Web-Ordner für die fertige Bilder
picture_temp_folder="tmp/"
printerID="Canon_CP800" #erster Drucker
pause_snaps=2 #Wartepause zwischen den Fotos in Sekunden (8,5)
##### Einstellungen ####

printer.resetPrinterJob()
dest="pose.jpg" 

printer.printFile(printerID,dest)
#stat=printer.printerStatus2(printerID)
#print("Status=" + stat)
#if not printer.printFile(printerID,dest):
#      printerID=printer.getNextPrinterID(printerID)
#      printer.printFile(printerID,dest)

print("fertig...")
