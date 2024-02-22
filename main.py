from adafruit_mqtt import *
import random
import time
feed_ids = ["button1", 	"button2", "humidity", "light", "temperature"]
username = "AI_ProjectHGL"
password = "aio_" + "CHRX08OBUahjbuHBFWdtmdIVwibh"

mqtt = Adafruit_MQTT(username, password, feed_ids)

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

