from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped
from typing import List

Base = declarative_base()

# Organization
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

# Role
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    permission_ids = Column(String, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")

# User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")

# Device
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    uuid = Column(String, nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    last_ping_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="devices")
    device_reason_logs = relationship("DeviceReasonLog", back_populates="device")

# Reason
class Reason(Base):
    __tablename__ = "reasons"
    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String, nullable=False)
    key_num = Column(Integer, nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    organization = relationship("Organization", back_populates="reasons")
    device_reason_logs = relationship("DeviceReasonLog", back_populates="reason")

# DeviceReasonLog
class DeviceReasonLog(Base):
    __tablename__ = "device_reason_logs"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    reason_id = Column(Integer, ForeignKey("reasons.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    device = relationship("Device", back_populates="device_reason_logs")
    reason = relationship("Reason", back_populates="device_reason_logs")

# DeviceLog
class DeviceLog(Base):
    __tablename__ = "device_logs"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    status_code = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
