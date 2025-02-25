import paho.mqtt.client as mqtt
import json

broker_ip = "192.168.31.229"  # Replace with your MQTT broker's IP address
topic="test"
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")

# Define the on_message callback
def on_message(client, userdata, msg):
    print(f"Received message from topic: {msg.topic}")
    print("Message:", msg.payload.decode("utf-8"))

# Create an MQTT client instance
client = mqtt.Client()
# Assign the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
print("Attempting to connect to the broker...")
try:
    client.connect(broker_ip, 1883, 60)
except Exception as e:
    print(f"Failed to connect to broker: {e}")

# Blocking call to process network traffic, dispatch callbacks, and handle reconnecting.
client.loop_forever()
