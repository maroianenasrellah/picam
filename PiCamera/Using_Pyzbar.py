from PIL import Image
from picamera import PiCamera
from time import sleep
import pyzbar.pyzbar as pyzbar

camera = PiCamera()
camera.resolution = (640, 480)
#camera.capture('/home/pi/PiCamera/image.jpg',resize=(320, 240))
file_path ='/home/pi/PiCamera/image.jpg'
while 1:
        
    try:
        camera.resolution = (640, 480)
        camera.start_preview()
        camera.preview_alpha = 124
        sleep(0.5)
        file_path ='/home/pi/PiCamera/image.jpg'
        camera.capture(file_path)
        camera.stop_preview()
        with open(file_path, 'rb') as image_file:
            image = Image.open(image_file)
            image.load()
            codes = pyzbar.decode(Image.open(file_path))
            if len(codes) != 0:
                camera.stop_preview()
                print('QR codes: %s' % codes)
            else:
                print("pas detection")
                camera.stop_preview()
                
                # camera.start_preview()

    except:
        print("erreur")
    
    
    