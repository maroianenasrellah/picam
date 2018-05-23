import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = (24, 1)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
##    camera.preview_fullscreen = True
    camera.preview_alpha = 128
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg', resize=(320, 240))