import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)


def openLight():
    GPIO.output(40, GPIO.HIGH)


def closeLight():
    GPIO.output(40, GPIO.LOW)

closeLight()