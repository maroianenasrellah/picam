#from qrtools import QR
from qrtools import *

myCode = QR(filename=u"/home/pi/bookmark.png")
if myCode.decode():
  print (myCode.data)
  print (myCode.data_type)
  print (myCode.data_to_string())