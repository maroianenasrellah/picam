#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import MySQLdb

continue_reading = True

##def read_data(backData):
##    #print("Traduction en ASCII : ", end='')
##    c= 0
##    while (c<16):
##        if(backData[c]!=0) :
##            try :
##                print(str(chr(backData[c])),end='')
##            except :
##                print(" Contenu Illisible")
##        c+=1
##    print("\n")

def h2str(entree):
    sortie=str(chr(entree))
    return sortie
def recup_date_val(dlv):
    Date_TEMP=""
    Date_TEMP_OUT=""	
    c= 1
    while (c<9):
        if(dlv[c]!=0):
            try :
                Date_TEMP=str(chr(dlv[c]))
                Date_TEMP_OUT=Date_TEMP_OUT+Date_TEMP
            except :
                print(" Contenu Illisible")
        c+=1
    return Date_TEMP_OUT

def read_card(backData):
    Datatemp = ""
    c =0
    while (c<16):
        if(backData[c]!=0):
            try:
                Datatemp=Datatemp+h2str(backData[c])
            except:
                print(" Contenu Illisible")
        c=c+1
    #print("\n")
    return Datatemp

def getdata(backData):
    
    GCP_CLIENT_CODE="yapo"
    
    return h2str(backData[0]),recup_date_val(backData),int(backData[9])*256+int(backData[10]),backData[11],GCP_CLIENT_CODE

def insert_passage(GCP_UID, GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE):
    try:
        db = MySQLdb.connect("127.0.0.1", "yapo", "pipi", "rpi")
        curs=db.cursor()
        
        print("#####################################################")
        print("GCP_UID: ",GCP_UID,"\n")
        print("Type Card",GCP_CARD_TYPE,"\n")
        print("NOM: ",GCP_NOM,"\n")
        print("PRENOM: ",GCP_PRENOM,"\n")
        print("CLUB: ",GCP_CLUB,"\n")
        print("Date Limite De Validité: ",GCP_DATE_VALID,"\n")
        print("Date Dernier Passage: ",GCP_DATE_PASSAGE,"\n")
        print("Crédit Cumulé: ",GCP_CREDIT,"\n")
        print("Unités Consommées",GCP_CONSO,"\n")
        print("MAX seaux par jour: ",GCP_JOUR_MAX,"\n")
        print("Unités Consommées du jour:",GCP_JOUR_USED,"\n")
        print("Code CLIENT :",GCP_CLIENT_CODE,"\n")
        print("#####################################################")
        
        query="INSERT INTO GCP SET GCP_UID='%s', GCP_CARD_TYPE='%s', GCP_NOM='%s', GCP_PRENOM='%s', GCP_CLUB='%s', GCP_DATE_VALID='%s', GCP_DATE_PASSAGE='%s',GCP_CREDIT='%s',GCP_CONSO='%s',GCP_JOUR_MAX='%s',GCP_JOUR_USED='%s',GCP_CLIENT_CODE='%s'" % (GCP_UID, GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
        curs.execute(query)
        db.commit()
        print("bien été ajouté !'")
        print("#####################################################")
        db.close()
    except MySQLdb.Error as err:
        print("Exception while MYSQL Connection")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            db.close()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            db.close()
        else:
            print(err)
            db.close()
            
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        GCP_UID=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])+str(uid[4])
        print("GCP_UID: ",GCP_UID)
        
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        # Authenticate
        print("..............................BLOC 1.....................................")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 4,keyA_Prive , uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            nomData=MIFAREReader.MFRC522_Read(4)
            nomtemp = read_card(nomData)
            prenomData = MIFAREReader.MFRC522_Read(5)
            prenomtemp = read_card(prenomData)
            societeData = MIFAREReader.MFRC522_Read(6)
            societetemp = read_card(societeData)
            print("\n")
        else:
            print ("Authentication error sur secteur 4")
            continue_reading = False
        
        # Authenticate
        print("..............................BLOC 2.....................................")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8,keyA_Prive, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            print("\n")
            print("Read Block 8")
            Data = MIFAREReader.MFRC522_Read(8)
            print("\n")
            TYPE_CARD=(getdata(Data)[0])
            DATE_CARD_VALID=(getdata(Data)[1])
            CREDIT_TOTAL=(getdata(Data)[2])
            NBR_SEAUX_MAX=(getdata(Data)[3])
            CODE=(getdata(Data)[4])
        else:
            print ("Authentication error sur secteur 8")
            continue_reading = False
        
        print("..............................BLOC 3.....................................")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12,keyA_Prive, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            print("\n")
            try:
                print("Read Block 12")
                Data = MIFAREReader.MFRC522_Read(12)
                CARD=(getdata(Data)[0])
                DATE_LAST_PASS=(getdata(Data)[1])
                CONSO_TOTAL=(getdata(Data)[2])
                CONSO_JOUR=(getdata(Data)[3])
                code=(getdata(Data)[4])
                
                #insertion dans La Base
                insert_passage(GCP_UID, TYPE_CARD, nomtemp,prenomtemp,societetemp,DATE_CARD_VALID,DATE_LAST_PASS,CREDIT_TOTAL,CONSO_TOTAL,NBR_SEAUX_MAX,CONSO_JOUR,CODE)
                MIFAREReader.MFRC522_StopCrypto1()
                #continue_reading = False
            except:
                print("Erreur de lecture...")
                continue_reading = False
                
            #insert_passage(GCP_UID, GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)
           
        else:
            print ("Authentication error sur secteur 12")


