import sys
from Adafruit_IO import MQTTClient

class Adafruit_MQTT:

    AIO_FEED_IDs = []
    AIO_USERNAME = ""
    AIO_KEY = ""
    client = None

    def __init__(self, username, key, feed_ids):
        self.AIO_FEED_IDs = feed_ids
        self.AIO_USERNAME = username
        self.AIO_KEY = key

        self.client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)

    def subscribe(self, client , userdata , mid , granted_qos):
        print("Subscribeb...")

    def disconnected(self, client):
        print("Disconnected...")
        sys.exit (1)

    def message(self, client , feed_id , payload):
        print("Received: " + payload + " at feed id: " + feed_id)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)



