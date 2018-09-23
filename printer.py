#!/usr/bin/python

from PIL import Image
import RPi.GPIO as GPIO, time, os, subprocess

def getActivePrinterID():
    command="lpstat" 
    #proc = subprocess.Popen(command, stderr=subprocess.STDOUT, shell=True)
    proc = subprocess.Popen(["lpstat","-p"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        x=x.decode("utf-8") 
        
        if x.split(" ")[0]=="printer":
            iD=x.split(" ")[1]
            command="cupsenable " + iD 
            gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            status=x.replace(iD,"")
            print("Drucker: " + iD + " ist " + status)

def resetPrinterJob():
    proc = subprocess.Popen("lpstat",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout :
        x=x.decode("utf-8") 
        #print (x)
        printID=x.split(" ")[0]
        command="cancel " + printID
        gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        
def printerStatus(printerID):
    proc = subprocess.Popen(["lpstat","-p",printerID],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        x=x.decode("utf-8") 
        
        print(x)
        if "disabled" in x or "idle" in x:
             return False
        else:
            return True

def printerStatus2(printerID):
    exit=True
    z=0
    while z<60:
        time.sleep(1)
        z=z+1
        proc = subprocess.Popen(["lpstat","-p",printerID],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for x in proc.stdout : 
            x=x.decode("utf-8") 
            print(x)
            if "Paper feed problem" in x:
                print ("Papier leer")
                return False
            elif "Ribbon depleted" in x:
                print("Farbkatusche leer")
                return False
            elif "disabled" in x:
                 print("ausgeschaltet")
                 return False
            elif "idle" in x:
                print("fertig")
                return True
                
def printFile(printerId,file):
    print("Druck auf " + printerId)
    resetPrinterJob()

    command="cupsenable " + printerId
    gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    
    #command="lp -d " + printerId + " " + file
    #gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    
    proc = subprocess.Popen(["lp","-d",printerId,file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        x=x.decode("utf-8") 
        #print(x)
        #print(x.split(" ")[3])
    
    #Status abfragen
    #time.sleep(10)
    return printerStatus2(printerId)

def getNextPrinterID(printerID):
    if printerID=="Canon_CP800":
        return "Canon_CP800_2"
    else:
        return "Canon_CP800"

