#!/usr/bin/python
#-*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
import RPi.GPIO as GPIO
import MFRC522
import smbus
import time
import datetime
import hexdump
import MySQLdb
import threading 
from threading import Thread
#################################################VARIABLES#################################################
##Bloc1
B1S4=4
B1S5=5
B1S6=6
##Bloc2
B2S8=8
##Bloc3
B3S12=12
############################################################################################################
bOkString="Debut"

keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74]
##caractéristique
CREDIT_TOTAL = 0
CONSO_JOUR = 0
CONSO_TOTAL = 0
NBR_SEAUX_MAX = 0
Solde=0

##LED
GPIO_LEDR = 36
GPIO_LEDV = 32
time_sleep_led=3

# relais
GPIO_relais = 40# le relais est branche sur la pin 40 / GPIO21
GPIO.setmode(GPIO.BOARD) # comme la librairie MFRC522
GPIO.setwarnings(False)
GPIO.setup(GPIO_relais, GPIO.OUT)# Define some device parameters
GPIO.setup(GPIO_LEDV, GPIO.OUT)
GPIO.setup(GPIO_LEDR, GPIO.OUT)

#################################################FONCTIONS#################################################
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
def msg(L1,L2):
	lcd_string(L1,LCD_LINE_1)
	lcd_string(L2,LCD_LINE_2)
	
I2C_ADDR  = 0x27
#I2C_ADDR  = 0x77# I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line


#LCD 
# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)
lcd_init()
lcd_byte(0x01,LCD_CMD)

######################################################################################################################
def h2str(entree):
    sortie=str(chr(entree))
    return sortie

def recup_date_val(dlv):
    Date_TEMP=""
    Date_TEMP_OUT=""	
    c= 1
    while (c<9):
        if(dlv[c]!=0):
            try:
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
######################################################################################################################
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
i=0

try:
    while True:
        i=i+1
        stoday = datetime.datetime.today()
        # Display Message
        lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
        lcd_string("Attente Carte",LCD_LINE_2)
        
        print("Attente Carte : ",i)
        # Scan for cards
        (bOK,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # If a card is found
        if bOK == MIFAREReader.MI_OK:
            bOkString="Carte detectee"
            print (bOkString)
        # Get the UID of the card
        (bOK,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        if bOK == MIFAREReader.MI_OK:
            # Print UID
            GCP_UID=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            
            bOkString="UID de la carte: "
            print (bOkString,GCP_UID)
            
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)
            # Authenticate with private key
            print("..............................BLOC 1.....................................")
            bOK = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B1S4,keyA_Prive, uid)
            # Check if authenticated
            if(bOK == MIFAREReader.MI_OK):
                bOkString="authentication successed"
                print(bOkString)
                try:
                    nomData= MIFAREReader.MFRC522_Read(B1S4)
                    GCP_NOM = read_card(nomData)
                except:
                    print("echec-lecture-secteur-",B1S4)
                    
                try:
                    prenomData = MIFAREReader.MFRC522_Read(B1S5)
                    GCP_PRENOM = read_card(prenomData)
                except:
                    print("echec-lecture-secteur-",B1S5)
                
                try:
                    societeData  = MIFAREReader.MFRC522_Read(B1S6)
                    GCP_CLUB = read_card(societeData)
                except:
                    print("echec-lecture-secteur-",B1S6)
                    
                print("\n")
                print("NOM: ",GCP_NOM,"\n")
                print("PRENOM: ",GCP_PRENOM,"\n")
                print("CLUB: ",GCP_CLUB,"\n")
            else:
                print("Error Authentification ",B1S4,"-Bloc 1")
                MIFAREReader.MFRC522_StopCrypto1()
                
            print("..............................BLOC 2.....................................")
            bOK = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B2S8,keyA_Prive, uid)
            # Check if authenticated
            if(bOK == MIFAREReader.MI_OK):
                bOkString="authentication successed"
                print(bOkString)
                try:
                    Data= MIFAREReader.MFRC522_Read(B2S8)
                    GCP_CARD_TYPE=(getdata(Data)[0])
                    DATE_CARD_VALID=(getdata(Data)[1])
                    CREDIT_TOTAL=(getdata(Data)[2])
                    NBR_SEAUX_MAX=(getdata(Data)[3])
                    GCP_CLIENT_CODE=(getdata(Data)[4])
                except:
                    print("echec-lecture-secteur-",B2S8)
                    
                print("\n")
                print("Type Card",GCP_CARD_TYPE,"\n")
            else:
                print("Error Authentification ",B2S8,"-Bloc 2")
                MIFAREReader.MFRC522_StopCrypto1()
                
            print("..............................BLOC 3.....................................")
            bOK = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B3S12,keyA_Prive, uid)
            # Check if authenticated
            if(bOK == MIFAREReader.MI_OK):
                bOkString="authentication successed"
                print(bOkString)
                try:
                    Data= MIFAREReader.MFRC522_Read(B3S12)
                    CARD=(getdata(Data)[0])
                    DATE_LAST_PASS=(getdata(Data)[1])
                    CONSO_TOTAL=(getdata(Data)[2])
                    CONSO_JOUR=(getdata(Data)[3])
                    GCP_CLIENT_CODE=(getdata(Data)[4])
                except:
                    print("echec-lecture-secteur-",B3S12)
                    
                print("\n")
                print("Date Dernier Passage: ",DATE_LAST_PASS,"\n")
                print("Unités Consommées",CONSO_TOTAL,"\n")
                print("Unités Consommées du jour:",CONSO_JOUR,"\n")
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print("Error Authentification ",B3S12,"-Bloc 3")
                MIFAREReader.MFRC522_StopCrypto1()      
                
except KeyboardInterrupt:
    lcd_string("MACHINE ARRETEE",LCD_LINE_1)
    lcd_string("ESSAYEZ + TARD",LCD_LINE_2)
    
