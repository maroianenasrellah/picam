from qrtools import QR

myCode = QR(filename="/home/me/Desktop/sample.png")
if myCode.decode():
  print (myCode.data)
  print (myCode.data_type)
  print (myCode.data_to_string())
else:
    print("erreur")