import RPi.GPIO as GPIO
from time import sleep
from Config import *

def buzzerpininit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer,GPIO.OUT)
    buzzing(0.4, 1)
    print ("Buzzer Initialized...")

def buzzing(dly,tms):
    print ("Buzzing Starting...")
    for i in range (tms):
        GPIO.output(buzzer,GPIO.HIGH)
        print ("Beep")
        sleep(dly)  
        GPIO.output(buzzer,GPIO.LOW)
        print ("No Beep")
        sleep(dly)
    #GPIO.cleanup()
    print ("Buzzing Done...")