from adafruit_mqtt import *
from uart import *

feed_ids = ["button1", 	"button2", "humidity", "light", "temperature"]
username = "AI_ProjectHGL"
password = "aio_" + "CHRX08OBUahjbuHBFWdtmdIVwibh"

mqtt = Adafruit_MQTT(username, password, feed_ids)
uart = Uart(115200, None, True)

while True:
    uart_data = uart.readSerial()
    if len(uart_data) > 0:
        for data in uart_data:
            if (data[1] == 'T'):
                temperature = data[2]
                mqtt.publish("temperature", temperature)
            elif (data[1] == 'H'):
                humidity = data[2]
                mqtt.publish("humidity", humidity)
            elif (data[1] == 'L'):
                light = data[2]
                mqtt.publish("light", light)
        uart.clearData()


