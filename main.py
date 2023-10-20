import xml.etree.ElementTree as ET
import requests
import paho.mqtt.client as mqtt
import schedule
import time

recording_state = None

def check_recording():
    try:
        url = "http://<vMIX IP ADDRESS>:8088/api"
        response = requests.get(url)
        root = ET.fromstring(response.text)
        recording = root.find("recording").text
        global recording_state
        if recording != recording_state:
            update_status(recording)
            recording_state = recording
    except requests.exceptions.ConnectionError:
        print("\rvMix disconnected, retrying connection...", end='', flush=True)
    except Exception as e:
        print(f"\rAn error occurred: {e}", end='', flush=True)

def send_mqtt_message(recording):
    try:
        if recording == "True":
            if not client.is_connected():
                client.connect("127.0.0.1", 1883, keepalive=60)
            result, mid = client.publish("zigbee2mqtt/<DEVICE>/set", '{"state": "On"}')
            if result != mqtt.MQTT_ERR_SUCCESS:
                print(f"\rError sending MQTT message: {result}", end='', flush=True)
        elif recording == "False":
            if not client.is_connected():
                client.connect("127.0.0.1", 1883, keepalive=60)
            result, mid = client.publish("zigbee2mqtt/<DEVICE>/set", '{"state": "Off"}')
            if result != mqtt.MQTT_ERR_SUCCESS:
                print(f"\rError sending MQTT message: {result}", end='', flush=True)
    except Exception as e:
        print(f"\rAn error occurred: {e}", end='', flush=True)

def update_status(recording):
    status_text = "vMix is currently recording." if recording == "True" else "vMix is currently Not recording."
    print(f"\r{status_text}", end='', flush=True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("127.0.0.1", 1883, 60)

# Initial check for recording status
check_recording()

schedule.every(1).seconds.do(check_recording)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
