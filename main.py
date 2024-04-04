from adafruit_mqtt import *
from uart import *

feed_ids = ["button1", 	"button2", "humidity", "light", "temperature"]
username = "AI_ProjectHGL"
password = "aio_" + "CHRX08OBUahjbuHBFWdtmdIVwibh"

mqtt = Adafruit_MQTT(username, password, feed_ids)
uart = Uart(115200, None, True)

while True:
    uart_data = uart.readSerial()
    if uart_data is not None:
        for i in range(len(uart_data)):
            if (uart_data[i] == 'T'):
                temperature = uart_data[i + 1]
                mqtt.publish("temperature", temperature)
            elif (uart_data[i] == 'H'):
                humidity = uart_data[i + 1]
                mqtt.publish("humidity", humidity)
            elif (uart_data[i] == 'L'):
                light = uart_data[i + 1]
                mqtt.publish("light", light)

