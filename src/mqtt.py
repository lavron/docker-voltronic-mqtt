import paho.mqtt.client as mqtt
import os

MQTT_SERVER = os.getenv('MQTT_SERVER')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

INVERTER_NAME = os.getenv('INVERTER_NAME', 'inverter')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX', 'homeassistant')
REPORT_INTERVAL_S = int(os.getenv('REPORT_INTERVAL_S', 1))


class MQTT:
    def __init__(self):
        self.topic_prefix = f"{MQTT_TOPIC_PREFIX}/sensor/{INVERTER_NAME}_"

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.connect_timeout = 60
        self.client.connect_async(MQTT_SERVER, MQTT_PORT, 60)
        self.client.loop_start()

    def publish(self, data):
        for query, sensors in data.items():
            for sensor, data in sensors.items():
                topic = f"{self.topic_prefix}{sensor}"
                value = data['value']
                print("👉topic", topic)
                print("👉value", value, type(value))
                self.client.publish(topic, value, qos=1)


    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")