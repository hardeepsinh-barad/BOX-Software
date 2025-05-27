import paho.mqtt.client as mqtt
import threading

BROKER = '122.169.104.145'
PORT = 8833
COMMAND_TOPIC = 'terminal/clear/command'
RESPONSE_TOPIC = 'terminal/clear/response'

response_buffer = []
response_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    client.subscribe(RESPONSE_TOPIC)

def on_message(client, userdata, msg):
    print(msg.payload.decode(), end='')
    response_event.set()

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            cmd = input("$ ")
            if cmd.strip().lower() == 'exit':
                break
            response_event.clear()
            client.publish(COMMAND_TOPIC, cmd)
            # Wait for response
            response_event.wait(timeout=5)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
