import paho.mqtt.client as mqtt
import time

# MQTT Broker settings (update as needed)
MQTT_BROKER = "192.168.1.34"  # Replace with your broker if necessary
MQTT_PORT = 1883
TOPIC = "test"  # Update the topic as per your application

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code:", rc)

def on_publish(client, userdata, mid):
    print("Message published. Message ID:", mid)

def get_message(reason: int) -> str:
    """
    Returns a message based on the reason code.
    Reason codes:
        1 -> Normal Stop
        2 -> Break
        3 -> Breakdown
    """
    if reason == 1:
        return "normal stop"
    elif reason == 2:
        return "break"
    elif reason == 3:
        return "breakdown"
    else:
        return ""

def main():
    # Create an MQTT client instance
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    # Wait briefly to establish connection
    time.sleep(1)

    # Prompt user for input: 1 for normal stop, 2 for break, 3 for breakdown
    try:
        reason = int(input("Enter reason (1 for normal stop, 2 for break, 3 for breakdown): "))
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        client.loop_stop()
        client.disconnect()
        return

    message = get_message(reason)
    if not message:
        print("Invalid reason selected. Please choose 1, 2, or 3.")
        client.loop_stop()
        client.disconnect()
        return

    # Publish the message to the specified topic
    result = client.publish(TOPIC, message)
    result.wait_for_publish()

    print(f"Published message: '{message}' to topic: '{TOPIC}'")

    # Cleanup: stop loop and disconnect
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
