import xml.etree.ElementTree as ET
import requests
import paho.mqtt.client as mqtt
import schedule
import time
import argparse

# Define your variables here
vMix_ip = "YOUR_VMIX_IP_ADDRESS"
mqtt_broker_ip = "YOUR_BROKER_IP_ADDRESS"
start_recording_topic = "YOUR_START_RECORDING_TOPIC"
stop_recording_topic = "YOUR_STOP_RECORDING_TOPIC"

recording_state = None

def check_recording():
    try:
        url = f"http://{vMix_ip}:8088/api"
        response = requests.get(url)
        root = ET.fromstring(response.text)
        recording = root.find("recording").text
        global recording_state
        if recording != recording_state:
            recording_state = recording
            update_status(recording)
            send_mqtt_message(recording)
    except requests.exceptions.ConnectionError:
        print("\rvMix disconnected, retrying connection...", end='', flush=True)
    except Exception as e:
        print(f"\rAn error occurred: {e}", end='', flush=True)

def send_mqtt_message(recording):
    try:
        client = mqtt.Client()
        client.connect(mqtt_broker_ip, 1883, keepalive=60)

        if recording == "True":
            result, mid = client.publish(start_recording_topic, '{"state": "On"}')
            if args.logs:
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print("\rMQTT message sent successfully.", end='', flush=True)
                else:
                    print(f"\rError sending MQTT message: {result.rc}", end='', flush=True)
        elif recording == "False":
            result, mid = client.publish(stop_recording_topic, '{"state": "Off"}')
            if args.logs:
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print("\rMQTT message sent successfully.", end='', flush=True)
                else:
                    print(f"\rError sending MQTT message: {result.rc}", end='', flush=True)
    except Exception as e:
        if args.logs:
            print(f"\rAn error occurred: {e}", end='', flush=True)

def update_status(recording):
    status_text = "vMix is currently recording." if recording == "True" else "vMix is currently Not recording."
    print(f"\r{status_text}", end='', flush=True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="vMix to MQTT Script")
parser.add_argument("--logs", "-l", action="store_true", help="Enable log messages")
args = parser.parse_args()

# Initial check for recording status
check_recording()
