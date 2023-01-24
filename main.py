import xml.etree.ElementTree as ET
import requests
import paho.mqtt.client as mqtt
import schedule
import time

recording_state = None

def check_recording():
    try:
        url = "http://[vMix IP]:8088/api"
        response = requests.get(url)
        root = ET.fromstring(response.text)
        recording = root.find("recording").text
        global recording_state
        if recording != recording_state:
            recording_state = recording
            send_mqtt_message(recording)
    except:
        print("vMix disconnected, retrying connection...")
        client.connect("[MQTT BROKER IP]", 1883, 60) # reconnect to vMix

def send_mqtt_message(recording):
    if recording == "True":
        print("vMix is currently recording.")
        client.publish("[MQTT TOPIC]", '{"state": "On"}')
    if recording == "False":
        print("vMix is currently Not recording.")
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
