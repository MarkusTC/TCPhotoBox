#!/usr/bin/python

from PIL import Image
import RPi.GPIO as GPIO, time, os, subprocess

def getActivePrinterID():
    command="lpstat" 
    #proc = subprocess.Popen(command, stderr=subprocess.STDOUT, shell=True)
    proc = subprocess.Popen(["lpstat","-p"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        if x.split(" ")[0]=="printer":
            iD=x.split(" ")[1]
            command="cupsenable " + iD 
            gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            status=x.replace(iD,"")
            print("Drucker: " + iD + " ist " + status)

def resetPrinterJob():
    proc = subprocess.Popen("lpstat",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        printID=x.split(" ")[0]
        command="cancel " + printID
        gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        
def printerStatus(printerID):
    proc = subprocess.Popen(["lpstat","-p",printerID],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        print(x)
        if "disabled" in x:
             return False
        else:
            return True

def printFile(printerId,file):
    print("Druck auf " + printerId)
    resetPrinterJob()

    command="cupsenable " + printerId
    gpout = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    
    proc = subprocess.Popen(["lp","-d",printerId,file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for x in proc.stdout : 
        print(x.split(" ")[3])
    #Status abfragen
    time.sleep(10)
    return printerStatus(printerId)

def getNextPrinterID(printerID):
    if printerID=="Canon_CP800":
        return "Canon_CP800_2"
    else:
        return "Canon_CP800"

