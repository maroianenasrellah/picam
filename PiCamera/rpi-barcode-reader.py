
import sys
import io
import time
import picamera
from PIL import Image
import zbar

# Create the in-memory stream
stream = io.BytesIO()
# create a reader
scanner = zbar.ImageScanner()
# configure the reader
scanner.parse_config('enable')

with picamera.PiCamera() as camera:
    #configure camera
    camera.video_stabilization = True
    camera.sharpness = 50
    camera.contrast = 30

    #start preview window
    camera.start_preview()

    #initialize stream reader
    stream = io.BytesIO()
    try:
        for foo in camera.capture_continuous(stream, format='jpeg'):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
            stream.truncate()
            stream.seek(0)

            # obtain image data
            pil = Image.open(stream).convert('L')
            width, height = pil.size
            raw = pil.tostring()

            # wrap image data
            image = zbar.Image(width, height, 'Y800', raw)

            # scan the image for barcodes
            scanner.scan(image)

            # extract results
            for symbol in image:
                # do something useful with results
                print ('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)

            # clean up
            del(image)

            #sleep to avoid 100% cpu usage
            time.sleep(0.05)
    finally:
        camera.stop_preview()