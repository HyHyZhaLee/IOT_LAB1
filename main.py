from adafruit_mqtt import *
import random
import time
import serial.tools.list_ports

feed_ids = ["button1", 	"button2", "humidity", "light", "temperature"]
username = "AI_ProjectHGL"
password = "aio_" + "CHRX08OBUahjbuHBFWdtmdIVwibh"

mqtt = Adafruit_MQTT(username, password, feed_ids)

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "/dev/pts/4"
    return commPort

portName = getPort()

print(portName)

while True:
    time.sleep(5)
    print("Publishing...")
    mqtt.publish("button1",random.randint(0,1))
    time.sleep(0.5)
    mqtt.publish("button2",random.randint(0,1))
    time.sleep(0.5)
    mqtt.publish("humidity",random.randint(0,100))
    time.sleep(0.5)
    mqtt.publish("temperature",random.randint(0,100))
    time.sleep(0.5)
    mqtt.publish("light",random.randint(0,100))
    pass

