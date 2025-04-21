import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from paho.mqtt.client import Client, CallbackAPIVersion
from app.models import Base, Reason, Device  # Assuming these are defined in models.py

# Configure DB connection
DATABASE_URL = "postgresql+psycopg2://admin1:admin@192.168.1.37:5432/iotbox1?sslmode=disable"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# MQTT Configuration
MQTT_BROKER = "192.168.1.37"
MQTT_PORT = 1883
MQTT_TOPIC = "cactus/+/reason"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to {MQTT_TOPIC}")
    else:
        print("❌ Failed to connect. Code:", rc)

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 3:
            print("⚠️ Invalid topic structure")
            return

        org, device_uuid, _ = topic_parts
        payload = json.loads(msg.payload.decode())
        print("payload:", payload)

        key = payload.get("key_num")
        timeStamp = payload.get("timestamp")

        if key is None or timeStamp is None:
            print("⚠️ Missing key or reason in payload")
            return

        session = SessionLocal()

        device = session.query(Device).filter_by(uuid=device_uuid).first()
        if not device:
            print("❌ Device not found for UUID:", device_uuid)
            return
        print(f"✅ Logged before session for device {device_uuid}")

        reason_entry = Reason(
            reason=timeStamp,
            key_num=key,
            org_id=device.org_id
        )
        session.add(reason_entry)
        print(f"✅ Logged epfnqeiurnhgeriu9bewriubnver session for device {device_uuid}")

        # Update last_ping_at timestamp for the device
        device.last_ping_at = datetime.utcnow()
        session.commit()
        print(f"✅ Logged reason for device {device_uuid}")

    except (json.JSONDecodeError, SQLAlchemyError) as e:
        print("❌ Error:", str(e))
    finally:
        session.close()

def main():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
