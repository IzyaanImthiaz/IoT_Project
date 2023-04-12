import Adafruit_DHT
from Config import *
 
def getdata():
  print ("Accessing Sensor...")
  humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, sensor)
  if humidity is not None and temperature is not None:
    print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
  else:
    print("Sensor failure. Check wiring.")
  print ("Sensor Closed...")
  return temperature, humidity