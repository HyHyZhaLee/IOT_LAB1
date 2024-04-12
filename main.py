from adafruit_mqtt import *
from uart import *

feed_ids = ["button1", 	"button2", "humidity", "light", "temperature"]
username = "AI_ProjectHGL"
password = "aio_" + "CHRX08OBUahjbuHBFWdtmdIVwibh"

uart = Uart(115200, None, True)


def processSubcribe(client, feed_id, payload):
    print("Proceesing subcribe with feed id: ", feed_id," + payload: ", payload)
    if feed_id == "button1":
        if payload == "1": uart.writeSerial("!1:B:1#")
        elif payload == "0": uart.writeSerial("!1:B:0#")
    elif feed_id == "button2":
        if payload == "1": uart.writeSerial("!2:B:1#")
        elif payload == "0": uart.writeSerial("!2:B:0#")


mqtt = Adafruit_MQTT(username, password, feed_ids)
mqtt.setOnMessageFunction(processSubcribe)

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


