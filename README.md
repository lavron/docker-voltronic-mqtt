MQTT interface for Voltronic(aka MPPSolar, Axpert, Powland, EASun. etc.) solar inverters.

# Exposed sensors:
- Inverter status
- Grid voltage
- Grid frequency
- Output load watt
- Battery capacity (SOC)
- Inverter heatsink temperature
- PV voltage

To run (edit as needed):
```bash
docker run -t -i --privileged -v /dev:/dev --restart=always --name voltronic-mqtt --pull=always -e \
MQTT_PASSWORD='your_password' -e \
MQTT_SERVER='your_server' -e \
MQTT_USER='your_username' -e \
SERIAL_PORT='/dev/ttyUSB0' \
lavron/voltronic-mqtt:latest
```
