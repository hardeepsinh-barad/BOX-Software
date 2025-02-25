import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:admin@localhost/iotbox1")
JWT_SECRET = os.getenv("JWT_SECRET", "harpal")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
MQTT_BROKER_ADDRESS="192.168.31.229"