import paho.mqtt.client as mqtt
import threading

# MQTT Configuration
MQTT_BROKER = '192.168.1.37'
MQTT_PORT = 1883
COMMAND_TOPIC = 'device/command'
RESPONSE_TOPIC = 'device/response'

# Global to store the latest response
latest_response = None
response_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(RESPONSE_TOPIC)

def on_message(client, userdata, msg):
    global latest_response
    latest_response = msg.payload.decode()
    response_event.set()

def main():
    global latest_response
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        while True:
            command = input("Enter a shell command (or 'exit' to quit): ").strip()
            if command.lower() == 'exit':
                break

            if command:
                response_event.clear()
                client.publish(COMMAND_TOPIC, command)
                print("Command sent. Waiting for response...\n")

                # Wait for a response or timeout after 5 seconds
                if response_event.wait(timeout=5):
                    print("Response received:\n")
                    print(latest_response)
                else:
                    print("No response received (timeout).\n")

    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
