import json
from datetime import datetime
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from paho.mqtt.client import Client
from app.models import Base, Reason, Device, DeviceReasonLog

# Configure DB connection
DATABASE_URL = "postgresql+psycopg2://admin1:admin@192.168.1.37:5432/iotbox1?sslmode=disable"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# MQTT Configuration
MQTT_BROKER = "192.168.1.37"
MQTT_PORT = 1883
MQTT_REASON_TOPIC = "cactus/+/reason"
MQTT_HEALTH_TOPIC = "cactus/+/health"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_REASON_TOPIC)
        client.subscribe(MQTT_HEALTH_TOPIC)
        print(f"📡 Subscribed to {MQTT_REASON_TOPIC}")
    else:
        print("❌ Failed to connect. Code:", rc)

def store_reason(payload, device_uuid):
    try:
        key_num = payload.get("key_num")
        timeStamp = payload.get("timestamp")

        if key_num is None or timeStamp is None:
            print("⚠️ Missing key or reason in payload")
            return

        session = SessionLocal()

        device = session.query(Device).filter_by(uuid=device_uuid).first()
        if not device:
            print("❌ Device not found for UUID:", device_uuid)
            return

        # Find the reason in the Reason table based on key_num and org_id
        reason = session.query(Reason).filter_by(key_num=key_num, org_id=device.org_id).first()
        if not reason:
            print(f"❌ Reason not found for key_num: {key_num} and org_id: {device.org_id}")
            return

        # Create a new DeviceReasonLog entry
        device_reason_log = DeviceReasonLog(
            device_id=device.id,
            reason_id=reason.id,
            org_id=device.org_id,
            timestamp=datetime.utcnow()
        )
        session.add(device_reason_log)
        session.commit()
        print(f"✅ Created DeviceReasonLog for device {device_uuid}, reason {reason.id}")

        # Update last_ping_at timestamp for the device
        device.last_ping_at = datetime.utcnow()
        session.commit()
        print(f"✅ Updated last_ping_at for device {device_uuid}")

    except (SQLAlchemyError) as e:
        print("❌ SQL Error:", str(e))
    finally:
        session.close()

def store_health(payload, device_uuid):
    try:
        session = SessionLocal()

        device = session.query(Device).filter_by(uuid=device_uuid).first()
        if not device:
            print("❌ Device not found for UUID:", device_uuid)
            return

        # Update last_ping_at timestamp for the device
        device.last_ping_at = datetime.utcnow()
        session.commit()
        print(f"✅ Updated last_ping_at for device {device_uuid}")
    except (SQLAlchemyError) as e:
        print("❌ SQL Error:", str(e))
    finally:
        session.close()

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 3:
            print("⚠️ Invalid topic structure")
            return

        org, device_uuid, topic = topic_parts
        print(f"📩 Received message on topic: {topic}")
        payload = json.loads(msg.payload.decode())

        if topic == "health":
            store_health(payload, device_uuid)
            print("Received health message:", payload)
            return
        elif topic == "reason":
            store_reason(payload, device_uuid)
        else:
            print("⚠️ Unknown topic:", topic)
            return      

    except (json.JSONDecodeError) as e:
        print("❌ JSON Error:", str(e))
   
def main():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
