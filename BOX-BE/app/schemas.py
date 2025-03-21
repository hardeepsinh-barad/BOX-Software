from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Organization schemas
class OrganizationBase(BaseModel):
    name: str
    email: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    class Config:
        orm_mode = True

# Role schemas
class RoleBase(BaseModel):
    name: str
    permission_ids: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    class Config:
        orm_mode = True

# Permission schemas
class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    class Config:
        orm_mode = True

# User schemas
class UserBase(BaseModel):
    org_id: int
    name: str
    contact_number: Optional[str] = None
    email: str
    role_id: int

class UserCreate(UserBase):
    password: str
    role_id: int  # Add this line

class UserUpdate(BaseModel):
    name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

# Device schemas
class DeviceBase(BaseModel):
    name: str
    uuid: str
    org_id: int
    last_ping_at: Optional[datetime] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    last_ping_at: datetime
    class Config:
        orm_mode = True

# OrgDeviceMap schemas
class OrgDeviceMapBase(BaseModel):
    org_id: int
    device_ids: str  # You can later change this to List[int] if you store JSON

class OrgDeviceMapCreate(OrgDeviceMapBase):
    pass

class OrgDeviceMap(OrgDeviceMapBase):
    id: int
    class Config:
        orm_mode = True

# Reason schemas
class ReasonBase(BaseModel):
    reason: str
    key_num: int
    org_id: int

class ReasonCreate(ReasonBase):
    pass

class Reason(ReasonBase):
    id: int
    class Config:
        orm_mode = True

# DeviceReasonLog schemas
class DeviceReasonLogBase(BaseModel):
    device_id: int
    reason_id: int
    org_id: int

class DeviceReasonLogCreate(DeviceReasonLogBase):
    pass

class DeviceReasonLog(DeviceReasonLogBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

# DeviceLog schemas
class DeviceLogBase(BaseModel):
    device_id: int
    status_code: int
    message: str

class DeviceLogCreate(DeviceLogBase):
    pass

class DeviceLog(DeviceLogBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True

# Token schemas
class TokenData(BaseModel):
    access_token: str
    token_type: str