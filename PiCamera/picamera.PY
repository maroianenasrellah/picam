from picamera import PiCamera
from time import sleep

camera = PiCamera()

##camera.start_preview()
##sleep(10)
##camera.capture('/home/pi/PiCamera/image.jpg')
##camera.stop_preview()

##
camera.start_preview()
##camera.annotate_background = Color('blue')
##camera.annotate_foreground = Color('yellow')
##camera.annotate_text = " Hello world "
##camera.exposure_mode = 'beach'
for i in range(100):
    #camera.image_effect = 'colorswap'
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    
camera.stop_preview()
