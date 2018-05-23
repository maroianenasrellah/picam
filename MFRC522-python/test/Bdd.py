#!/usr/bin/python
#-*- coding: utf-8 -*-
from datetime import datetime
import RPi.GPIO as GPIO
import MFRC522
import smbus
import time
import datetime
import hexdump
import MySQLdb

##quer ="INSERT INTO `rpi`.`GCP`(`GCP_UID`,`GCP_CARD_TYPE`,`GCP_NOM`,`GCP_PRENOM`,`GCP_CLUB`,`GCP_DATE_VALID`,`GCP_DATE_PASSAGE`,`GCP_CREDIT`,`GCP_CONSO`,`GCP_JOUR_MAX`,`GCP_JOUR_USED`,`GCP_CLIENT_CODE`)VALUES(21,'A','maroiane','nasrellah','yapo','20180516','20180515','15','0',5,'1','1994')";


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
        print("bien été ajouté !'")
        db.commit()
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

today = datetime.datetime.today() 
str_today =today.strftime("%Y%m%d")

GCP_UID=""
GCP_CARD_TYPE="C"
GCP_NOM="NASRELLAH"
GCP_PRENOM="MAROIANE"
GCP_CLUB="YAPO"
GCP_DATE_VALID=str_today
GCP_DATE_PASSAGE=str_today
GCP_CREDIT=20
GCP_CONSO=10
GCP_JOUR_MAX=15
GCP_JOUR_USED=5
GCP_CLIENT_CODE="1994"

insert_passage(str(GCP_UID), GCP_CARD_TYPE, GCP_NOM,GCP_PRENOM,GCP_CLUB,GCP_DATE_VALID,GCP_DATE_PASSAGE,GCP_CREDIT,GCP_CONSO,GCP_JOUR_MAX,GCP_JOUR_USED,GCP_CLIENT_CODE)