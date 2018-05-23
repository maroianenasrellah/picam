bOK=True
        if bOK:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                bOK=True
                bOk="Carte detectee"
            
            if bOK:
                bOK=False
                print(bOk)
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
        
        if status == MIFAREReader.MI_OK:
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)
            
            GCP_UID=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            
            bOK=True
            bOk="uid: "+GCP_UID
            
##        #authentication
##        if bOK:
##            print(bOk)
##            try:
##                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B1S4,keyA_Prive, uid)
##                bOK=True
##                bOk="Authentification  successed"
##            except:
##                bOK=False
##                
##        if bOK:
##            print(bOk)
##            print("..............................BLOC 1.....................................")
##            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B1S4,keyA_Prive, uid)
##            if(status == MIFAREReader.MI_OK):
##                bOK=True
##                bOk="Authentification  successed"
##            else:
##                bOK=False
##                bOk="Erreur Authentification"
##        if bOK:
##            
##            print(bOk)
            
            
from datetime import datetime
>>> past = datetime.now()
>>> present = datetime.now()
>>> past < present
True
>>> datetime(3000, 1, 1) < present
False
>>> present - datetime(2000, 4, 4)
datetime.timedelta(4242, 75703, 762105)