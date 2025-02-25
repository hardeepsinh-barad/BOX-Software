import json
import paho.mqtt.client as mqtt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import config

router = APIRouter()

class MqttMessage(BaseModel):
    topic: str
    message: dict

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        raise HTTPException(status_code=500, detail="MQTT connection failed")

def send_mqtt_message(topic: str, message: dict):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(config.MQTT_BROKER_ADDRESS, 1883, 60)  # Use the MQTT broker address from the config file
    client.loop_start()
    client.publish(topic, json.dumps(message))
    client.loop_stop()

@router.post("/send-mqtt/")
async def send_mqtt(mqtt_message: MqttMessage):
    try:
        send_mqtt_message(mqtt_message.topic, mqtt_message.message)
        return {"status": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
