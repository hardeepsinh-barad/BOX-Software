import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker settings
broker = "192.168.1.37"  # or use the IP address or hostname of your MQTT broker
port = 1883
topic = "test"

# Create MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker, port, 60)

# Loop to continuously send messages
try:
    while True:
        message = {"reading": 19.5}
        payload = json.dumps(message)
        client.publish(topic, payload)
        print(f"Sent: {payload}")
        time.sleep(1)  # Send every 1 second
except KeyboardInterrupt:
    print("Stopped by user")

# Disconnect cleanly
client.disconnect()
