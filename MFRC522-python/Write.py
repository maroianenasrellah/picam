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

continue_reading = True

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

        # Print UID
        print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        keyA_Privé = [0x59,0x61,0x50,0x6F,0x54,0x74]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        print("\n")
        print("............Authenticate sur Bloc 2 Secteur 8............")
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, keyA_Privé, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            print ("Sector 8 looked like this:")
            # Read block 8
            MIFAREReader.MFRC522_Read(8)
            print ("\n")
            
            print ("Sector 9 looked like this:")
            # Read block 9
            MIFAREReader.MFRC522_Read(9)
            print ("\n")
            
            print ("Sector 10 looked like this:")
            # Read block 10
            MIFAREReader.MFRC522_Read(10)
            print ("\n")

            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                data.append(0x00)

            print ("Sector 8 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(8, data)
            print ("\n")
            
            print ("Sector 9 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(9, data)
            print ("\n")
            
            print ("Sector 10 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(10, data)
            print ("\n")
            
            print ("Sector 8 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(8)
            print ("\n")
            
            print ("Sector 9 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(9)
            print ("\n")
            
            print ("Sector 10 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(10)
            print ("\n")

            # Stop
            #MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print ("Authentication error sur Bloc 2 Secteur 8")

        print("............Authenticate sur Bloc 3 Secteur 12............")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12, keyA_Privé, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            data = []

            print ("Sector 12 looked like this:")
            # Read block 12
            MIFAREReader.MFRC522_Read(12)
            print ("\n")
            
            print ("Sector 13 looked like this:")
            # Read block 13
            MIFAREReader.MFRC522_Read(13)
            print ("\n")
            
            print ("Sector 14 looked like this:")
            # Read block 14
            MIFAREReader.MFRC522_Read(14)
            print ("\n")

            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                data.append(0x00)

            print ("Sector 12 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(12, data)
            print ("\n")
            
            print ("Sector 13 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(13, data)
            print ("\n")
            
            print ("Sector 14 Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(14, data)
            print ("\n")
            
            print ("Sector 12 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(12)
            print ("\n")
            
            print ("Sector 13 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(13)
            print ("\n")
            
            print ("Sector 14 It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(14)
            print ("\n")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print ("Authentication error sur Bloc 3 Secteur 12")
