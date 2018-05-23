#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import MFRC522
import smbus
import datetime
import sushi
import hexdump

exec(open("/home/pi/MFRC522-python/sushi.py").read())
##execfile("/home/pi/New/sushi.py")


# relais
GPIO_relais = 40 # le relais est branché sur la pin 32 / GPIO12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # comme la librairie MFRC522
GPIO.setup(GPIO_relais, GPIO.OUT)

# Define some device parameters
##I2C_ADDR = 0x27 ou 0x3f #Afficheur de Xavier I2C device address, if any error, change this address to 0x3f
I2C_ADDR = 0x27
LCD_WIDTH = 16   # Maximum characters per line

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

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

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

def declencher_relais():
    GPIO.output(GPIO_relais, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GPIO_relais, GPIO.HIGH)
    
def h2str(entree):
    sortie=str(chr(entree))
    return sortie

def int_to_bytes(x,length):
    #return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    return x.to_bytes(length, 'big')

def to_bytes(n, length):
    return bytes( (n >> i*8) & 0xff for i in reversed(range(length)))
##
##def ######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData,Bloc):
##    #print("######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion en ASCII : ")
##    if Bloc == 8:
##        if(str(chr(backData[0]))=='A'):
##            print("Type Carte: Abonnement\n")
##        else:
##            print("Type Carte: Compteur\n")
##        print("Date Limite De Validité:",end='')
##        c= 1
##        while (c<9):
##            if(backData[c]!=0) :
##                try :
##                    print(str(chr(backData[c])),end='')
##                except:
##                    print("Contenu Illisible")
##            c+=1
##        print("\n")
##        print("CREDIT",int(backData[9])*256+int(backData[10]))
##        print("MAX",int(backData[11]))
##        i=12
##        print("Code Client: ",end='')
##        while (i<16):
##            print(str(chr(backData[i])),end='')
##            i+=1
##            
##    if Bloc == 12:
##        #print("X: ",str(chr(backData[0])))
##        print("Date Dernier Passage:",end='')
##        c= 1
##        while (c<9):
##            if(backData[c]!=0) :
##                try :
##                    print(str(chr(backData[c])),end='')
##                except:
##                    print("Contenu Illisible")
##            c+=1
##        print("\n")
##        print("CONSO",int(backData[9])*256+int(backData[10]))
##        print("NB",int(backData[11]))
##        print("YAPO")
##        print("\n")
                    
#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

# Initialise display
lcd_init()
##keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Looking for cards")
print("Press Ctrl-C to stop.")
print("\n") 
# This loop checks for chips. If one is near it will get the UID
try:
   
  while True:
      
    # Date
    stoday = datetime.datetime.today()
    # Display Message
    lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
    lcd_string("Attente Cartine",LCD_LINE_2)
    
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"   

    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

     # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
         # Print UID
        print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        lcd_string(""+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]),LCD_LINE_2)
        keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
        
        MIFAREReader.MFRC522_SelectTag(uid)   
        
        Bloc = 12
        print("##############################    Bloc 12   ##############################")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, Bloc,keyA_Prive, uid)
    
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            print("\nLecture...bloc 12")
            backData12 = MIFAREReader.MFRC522_Read(12)
            print("\n")
           # ######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)
            date_du_jour = stoday.strftime("%Y%m%d")
            conso=to_bytes(0,2)
            nb=to_bytes(0,1)
            s = b"X"+date_du_jour.encode()+conso+nb+b"YAPO"
            #print("s : ",hexdump.dump(s,sep=":"))                   
            MIFAREReader.MFRC522_Write(12,s)
            MIFAREReader.MFRC522_Write(13,s)
            MIFAREReader.MFRC522_Write(14,s)
            #
            #print("Ecriture terminée")
            print("\n")
            #print("Lecture...bloc 12 après Ecriture")
            backData1 = MIFAREReader.MFRC522_Read(12)
            #print("Lecture terminée")
            print("\n")
            ######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)
            
        else:
            print ("Authentication error sur secteur bloc",Bloc)
            
        print("\n")
        Bloc = 8
        print("##############################    Bloc 8   ##############################")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, Bloc,keyA_Prive, uid)
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            
            lcd_string(""+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]),LCD_LINE_2)
            print("\nLecture...bloc 8")
            backData8 = MIFAREReader.MFRC522_Read(8)
            print("\n")
            ######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData8,Bloc)
            date_Valid=b"20190515"
            credit=to_bytes(250,2)
            maxseau=to_bytes(100,1)
            code_Client=b"CODE"
            print("\n")
            #s = b"X" +  + (conso).to_bytes(2, byteorder='big') + (maxseau).to_bytes(1, byteorder='big')+b"YAPO"
            s =b"A"+date_Valid+credit+maxseau+code_Client
            #print("s : ",hexdump.dump(s,sep=":"))
            MIFAREReader.MFRC522_Write(8,s)
            MIFAREReader.MFRC522_Write(9,s)
            MIFAREReader.MFRC522_Write(10,s)
            print("Ecriture terminée")
            print("\n")
            
            print("Lecture...bloc 8 après Ecriture")
            backData = MIFAREReader.MFRC522_Read(8)
            #print("Lecture terminée")
            print("\n")
            ######Traduction_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData12,Bloc)tion_ASCII(backData8,Bloc)
          # Déclencher relais
            declencher_relais()
            
            MIFAREReader.MFRC522_StopCrypto1()
            
          # Attendre 2 secondes
            time.sleep(2)
        else:
            print ("Authentication error sur secteur bloc",Bloc)
            
except KeyboardInterrupt:
    lcd_string("MACHINE ARRETEE",LCD_LINE_1)
    lcd_string("ESSAYEZ + TARD",LCD_LINE_2)
    GPIO.cleanup()
