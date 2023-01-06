# Complete project details at https://RandomNerdTutorials.com

import esp
import machine
import micropython
import network
import sys
import time
import ubinascii

from umqttsimple import MQTTClient

esp.osdebug(None)
import gc

gc.collect()

ssid = 'ncsu'
password = None
mqtt_server = 'broker.hivemq.com'

client_id = ubinascii.hexlify(machine.unique_id())

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

client = MQTTClient(client_id, mqtt_server, keepalive=0)
client.set_last_will("fwh2200/c10/STATUS/esp32", b"offline", retain=True, qos=1)

try:
    client.connect()
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

print("Connected to broker")
