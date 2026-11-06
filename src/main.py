import os
import time

from voltronic import Voltronic
from mqtt import MQTT

REPORT_INTERVAL_S = float(os.getenv("REPORT_INTERVAL_S", 1))
QUERIES = ("QMOD", "QPIGS", "QPIWS")

inverter = Voltronic()
client = MQTT()


def loop():
    while True:
        if inverter.poll(QUERIES):
            client.publish(inverter.sensors)

        time.sleep(REPORT_INTERVAL_S)


if __name__ == "__main__":
    loop()
