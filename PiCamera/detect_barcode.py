import sys
import qrcode 
d = qrcode.Decoder()
if d.decode('out.png'):
    print ('result: ' + d.result)
else:
    print ('error: ' + d.error)