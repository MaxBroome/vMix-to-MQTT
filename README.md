# vMix to MQTT Script

This Python script allows you to monitor the recording status of vMix, a live production and streaming software, and send MQTT messages based on its recording state. You can customize the MQTT messages and topics to integrate vMix with your home automation or other applications.

## Prerequisites

Before using this script, make sure you have the following prerequisites:

1. **Python**: You need to have Python installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

2. **Required Python Libraries**: This script uses the following Python libraries, which can be installed using pip:

    - `xml.etree.ElementTree`
    - `requests`
    - `paho.mqtt.client`
    - `schedule`

    You can install these libraries using the following command:

    ```bash
    pip install xml.etree.ElementTree requests paho-mqtt schedule
    ```

3. **vMix**: You need to have vMix installed and running with its API enabled on port 8088.

4. **MQTT Broker**: Set up an MQTT broker and have its IP address ready, as you'll need it to configure the script.

## Customization

You need to customize the script with your specific configuration:

1. Replace the following variables with your own values:

    - `vMix_ip`: Set this to your vMix server's IP address.
    - `mqtt_broker_ip`: Set this to the IP address of your MQTT broker.
    - `start_recording_topic`: Set this to the MQTT topic where you want to send the "start recording" message.
    - `stop_recording_topic`: Set this to the MQTT topic where you want to send the "stop recording" message.

2. You can also customize the MQTT message payloads by modifying the `send_mqtt_message` function, the default is to turn the device On when recording, and Off when not.

## Usage

To use this script, follow these steps:

1. Clone or download this repository to your local machine.

2. Install the necessary libraries stated previously

3. Customize the script as described in the "Customization" section.

4. Open a terminal and navigate to the folder where you saved the script.

5. Run the script using the following command:

    ```bash
    python3 main.py
    ```

The script will monitor vMix's recording status and send MQTT messages to the specified topics whenever the recording state changes.

## Command-line Options

- `--logs` or `-l`: Enable log messages. If enabled, the script will display additional information for debugging purposes.

## Notes

- The script uses the `schedule` library to periodically check vMix's recording status. By default, it checks every 10 seconds. You can modify the schedule as needed in the `check_recording` function.

- The script will continuously run in the terminal until you manually stop it (e.g., by pressing Ctrl+C).

- Make sure the MQTT broker is running and accessible from the machine where you run the script.

- This script is designed to run on a continuous basis. You can use tools like `systemd` (on Linux) or `Task Scheduler` (on Windows) to ensure it runs automatically when your system starts.

- Monitor the script's console output for information about the recording status and MQTT messages.

With :heart: from Max Broomfield
