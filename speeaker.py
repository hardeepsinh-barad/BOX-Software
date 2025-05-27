import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker details
broker = "192.168.1.37"
port = 1883
topic = "cactus/speaker"

# MQTT client setup
client = mqtt.Client()

def connect_mqtt():
    client.connect(broker, port)
    client.loop_start()

def send_power_command(power_value):
    payload = json.dumps({"power": power_value})
    client.publish(topic, payload)
    print(f"Sent: {payload}")

if __name__ == "__main__":
    connect_mqtt()
    
    while True:
        cmd = input("Enter 1 to turn ON relay, 0 to turn OFF relay, or q to quit: ").strip()
        if cmd == '1':
            send_power_command(1)
        elif cmd == '0':
            send_power_command(0)
        elif cmd.lower() == 'q':
            break
        else:
            print("Invalid input. Use 1, 0, or q.")
    
    client.loop_stop()
    client.disconnect()
