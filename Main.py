from time import time, sleep
from Hardware.Buzzer import buzzing, buzzerpininit
from Hardware.Servo import servopininit, SetAngle
from Hardware.Sensor import getdata
from Hardware.MQTT_Publish import SendData
from Config import *
from Hardware.Predict import forecst
import datetime

def heat_index(t, rh):
    print("Calculating Heat Index...")
    print("Temp={0:0.1f}F Humidity={1:0.1f}%".format(t, rh))
    heat_index = -42.379 + 2.04901523*t + 10.14333127*rh - 0.22475541*t*rh - 0.00683783*t*t - 0.05481717*rh*rh + 0.00122874*t*t*rh + 0.00085282*t*rh*rh - 0.00000199*t*t*rh*rh
    print('Current heat index is {}F'.format(heat_index))
    print("Heat Index Calculated...")
    return heat_index

def map_val(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

buzzerpininit()
servopininit()

buzzing(0.2,3)

systim = time()
systim2 = time()
sense_interval = 0
hi = 0
buzz_interval = 0
buzz = False
level = 0

while True:

    if (time() - systim >= sense_interval):
        temperature, humidity = getdata()
        if humidity is not None or temperature is not None:
            temperatureF = (temperature*9/5) + 32
            hi = heat_index(temperatureF, humidity)
            
            angle = map_val(hi, hi_lowlimit, hi_highlimit, servo_minangle, servo_maxangle)
            
            if (angle >= 50):
                SetAngle(60, angle)
            elif (angle >= 25):
                SetAngle(55, angle)
            else:
                SetAngle(53, angle)
            
            SendData("sensedata/t", temperature)
            SendData("sensedata/rh", humidity)
            SendData("sensedata/hi", hi)

            date_object = datetime.date.today()
            enddate_object = date_object.replace(year=date_object.year + prediction_year_range)
            startdate_object = date_object.replace(year=date_object.year - prediction_year_range)
            
            startdate_string = startdate_object.strftime('%Y-%m-%d')
            enddate_string = enddate_object.strftime('%Y-%m-%d')

            avg_rh = forecst(model_loc, 'avg_rh', humidity, startdate_string, enddate_object)
            SendData("forecast/avg_rh", str(avg_rh))
          
            sense_interval = 60
            systim = time()
        else:
            hi = 0
            buzzing(0.1,10)
            SetAngle(60, 0)
            sense_interval = 5
            systim = time()

    if (hi >= 80 and hi < 90):
        buzz = True
        buzz_interval = 10
        level = 1
    elif (hi >= 90 and hi < 103):
        buzz = True
        buzz_interval = 5
        level = 2
    elif (hi >= 103 and hi < 124):
        buzz = True
        buzz_interval = 3
        level = 3
    elif (hi >= 125):
        buzz = True
        buzz_interval = 1
        level = 4
    else:
        print("Buzzing Stopped...")
        buzz = False
        level = 0

    if (buzz and (time() - systim2 >= buzz_interval)):
        print("Heat Index is at Level " + str(level))
        buzzing(0.2, 2)
        systim2 = time()
