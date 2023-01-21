import xml.etree.ElementTree as ET
import requests
import paho.mqtt.client as mqtt
import schedule
import time

# Connect to the vMix API
def check_recording():
    url = "http://[VMIX IP]:8088/api"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    recording = root.find("recording").text
    if recording == "True":
        print("vMix is currently recording.")
        client.publish("[MQTT TOPIC]", '{"state": "On"}')
    else:
        print("vMix is not currently recording.")
        client.publish("[MQTT TOPIC]", '{"state": "Off"}')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("[MQTT BROKER IP]", 1883, 60)

schedule.every(1).seconds.do(check_recording)

while True:
    schedule.run_pending()
    time.sleep(1)
