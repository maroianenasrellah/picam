#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import time

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
secteurBloc=eval(input("Entrez un Secteur :\n"))

##data = []
##texte = input("Entrez une chaine de caractère :\n")
##for c in texte:
##    if (len(data)<16):
##        data.append(int(ord(c)))
##while(len(data)!=16):
##    data.append(0)

print ("Placez votre carte RFID")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Une carte est detectee
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Recuperation UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        #data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        #data = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"

        # Print UID
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBloc, keyA_Prive, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            print("...................",secteurBloc,"...................")
            MIFAREReader.MFRC522_Read(secteurBloc)
            print ("\n")

            data = []
            strx ="NASRELLAH"
            for c in strx:
                if (len(data)<16):
                    data.append(int(ord(c)))
            while(len(data)!=16):
                data.append(0)
  
            print ("Ecriture ...")
            MIFAREReader.MFRC522_Write(secteurBloc, data)
            print ("\n")

            print ("Le secteur",secteurBloc," contient maintenant : ")
            MIFAREReader.MFRC522_Read(secteurBloc)
            print ("\n")
            print("...................",secteurBloc+1,"...................")
            MIFAREReader.MFRC522_Read(secteurBloc+1)
            print ("\n")
            
            data = []
            strx ="MAROIANE"
            for c in strx:
                if (len(data)<16):
                    data.append(int(ord(c)))
            while(len(data)!=16):
                data.append(0)
                
            print ("Ecriture ...")
            MIFAREReader.MFRC522_Write(secteurBloc+1, data)
            print ("\n")
            
            print ("Le secteur ",secteurBloc+1,"contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBloc+1)
            print ("\n")
            print("...................",secteurBloc+2,"...................")
            MIFAREReader.MFRC522_Read(secteurBloc+2)
            print ("\n")
            
            data = []
            strx ="yapo"
            for c in strx:
                if (len(data)<16):
                    data.append(int(ord(c)))
            while(len(data)!=16):
                data.append(0)
                
            print ("Ecriture ...")
            MIFAREReader.MFRC522_Write(secteurBloc+2, data)
            print ("\n")
            
            print ("Le secteur ",secteurBloc+2,"contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBloc+2)
            print ("\n")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()
            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print ("Authentication error with ",keyA_Prive)
            continue_reading = False
            
