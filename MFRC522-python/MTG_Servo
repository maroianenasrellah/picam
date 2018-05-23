from PIL import Image
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import sys

servoPin=18
miniServoPin=24
camera = PiCamera()
set_name = sys.argv[1]

def camera_setup(camera):
	camera.color_effects = (128,128)
	camera.rotation = 90
	camera.resolution = (300,100)


def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(servoPin,GPIO.OUT)
	GPIO.setup(miniServoPin,GPIO.OUT)

setup()
camera_setup(camera)

servo=GPIO.PWM(servoPin,50)
miniServo=GPIO.PWM(miniServoPin,50)
miniServo.start(2.5)
time.sleep(1)

while True:
	servo.start(2.5)
	time.sleep(1.5)
	servo.stop()
	timestamp=time.strftime("%Y%m%d%H%M%S")
	camera.capture(set_name+"/"+set_name+"_"+timestamp+".jpg")
	print "Picture Taken! See {0}_{1}.jpg!".format(set_name,timestamp)
	miniServo.ChangeDutyCycle(7.5)
	time.sleep(1)
	miniServo.ChangeDutyCycle(2.5)

GPIO.cleanup()