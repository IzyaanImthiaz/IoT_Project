import RPi.GPIO as GPIO
from time import sleep
from Config import *

def servopininit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo, GPIO.OUT)
    SetAngle(50, servo_minangle)
    sleep(1)
    SetAngle(50,servo_maxangle)
    sleep(1)
    SetAngle(50, servo_minangle)
    sleep(1)
    print ("Servo Initialized...")

def SetAngle(speed,angle):
    print ("Servo Positioning Starting...")
    pwm=GPIO.PWM(servo, speed)
    pwm.start(0)
    duty = angle / 18 + 2
    print ("Angle = " + str(angle) + " | Duty = " + str(duty))
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.2)
    GPIO.output(servo, False)
    pwm.stop()
    #GPIO.cleanup()
    print ("Servo Positioning Done...")