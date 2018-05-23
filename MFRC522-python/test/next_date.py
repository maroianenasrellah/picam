from datetime import datetime
from datetime import date
import datetime

today = date.today()
#print(date(today.year + 1, today.month, today.day))

DATE_CARD_VALID=date(today.year + 1, today.month, today.day).strftime("%Y%m%d")
print("Date Limite De Validité: ",DATE_CARD_VALID)

today = datetime.datetime.today() 
DATE_LAST_PASS =today.strftime("%Y%m%d %H:%M:%S")
        
print("Date du jour: ",DATE_LAST_PASS)


#Date Dernier Passage
DATE_LAST_PASS=stoday.strftime("%Y%m%d %H:%M:%S")
print("Date Dernier Passage: ",DATE_LAST_PASS)




