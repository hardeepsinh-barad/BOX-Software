import asyncio
import paho.mqtt.client as mqtt
from app.database import async_session  # Your async session from FastAPI setup
from app import models

MQTT_BROKER = "192.168.1.34"
MQTT_PORT = 1883
TOPIC = "test"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    # Decode the payload and extract information
    data = msg.payload.decode()
    print(f"Received message: {data} on topic: {msg.topic}")
    
    # You can parse the message further if needed (for example, extract reason info)
    asyncio.run(store_mqtt_data(data))

async def store_mqtt_data(data: str):
    async with async_session() as session:
        # Create a new DeviceData record
        device_data = models.DeviceData(message=data)
        session.add(device_data)
        await session.commit()
        print("Data stored in database:", data)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()
