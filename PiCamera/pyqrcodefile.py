import pyqrcode
qr = pyqrcode.create("HORN O.K. PLEASE.")
qr.png("horn.png", scale=6)

#import qrtools
from qrtools.qrtools import QR
qr = qrtools.QR()
qr.decode("horn.png")
print (qr.data)