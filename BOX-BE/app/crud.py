from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from app.auth import get_password_hash
import logging
from sqlalchemy.orm import selectinload, joinedload
from typing import List, Optional
from sqlalchemy import func, cast, Integer
from sqlalchemy.sql import expression


logger = logging.getLogger(__name__)
# ---------------------------
# Organization CRUD
# ---------------------------
async def get_organization(db: AsyncSession, org_id: int):
    result = await db.execute(select(models.Organization).where(models.Organization.id == org_id))
    return result.scalars().first()

async def get_organization_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Organization).where(models.Organization.name == name))
    return result.scalars().first()

async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    # Subquery to count devices per organization
    device_counts = (
        select(
            models.Device.organization_id,
            func.count(models.Device.id).label("device_count")
        )
        .group_by(models.Device.organization_id)
        .alias("device_counts")
    )

    # Main query to fetch organizations and their device counts
    query = (
        select(
            models.Organization,
            device_counts.c.device_count
        )
        .outerjoin(device_counts, models.Organization.id == device_counts.c.organization_id)
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)
    organizations = []
    for org, device_count in result.all():
        org_data = schemas.Organization.from_orm(org)
        org_data.device_count = device_count or 0  # Use 0 if device_count is None
        organizations.append(org_data)
    return organizations

async def create_organization(db: AsyncSession, organization: schemas.OrganizationCreate):
    db_org = models.Organization(**organization.dict())
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def update_organization(db: AsyncSession, org_id: int, organization: schemas.OrganizationCreate):
    db_org = await get_organization(db, org_id)
    if db_org:
        for key, value in organization.dict().items():
            setattr(db_org, key, value)
        await db.commit()
        await db.refresh(db_org)
    return db_org

async def delete_organization(db: AsyncSession, org_id: int):
    db_org = await get_organization(db, org_id)
    if db_org:
        await db.delete(db_org)
        await db.commit()
    return db_org

# ---------------------------
# Role CRUD
# ---------------------------
async def get_role(db: AsyncSession, role_id: int):
    result = await db.execute(select(models.Role).where(models.Role.id == role_id))
    return result.scalars().first()

async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Role).offset(skip).limit(limit))
    return result.scalars().all()

async def create_role(db: AsyncSession, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def update_role(db: AsyncSession, role_id: int, role: schemas.RoleCreate):
    db_role = await get_role(db, role_id)
    if db_role:
        for key, value in role.dict().items():
            setattr(db_role, key, value)
        await db.commit()
        await db.refresh(db_role)
    return db_role

async def delete_role(db: AsyncSession, role_id: int):
    db_role = await get_role(db, role_id)
    if db_role:
        await db.delete(db_role)
        await db.commit()
    return db_role

# ---------------------------
# Permission CRUD
# ---------------------------
async def get_permission(db: AsyncSession, permission_id: int):
    result = await db.execute(select(models.Permission).where(models.Permission.id == permission_id))
    return result.scalars().first()

async def get_permissions(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Permission).offset(skip).limit(limit))
    return result.scalars().all()

async def create_permission(db: AsyncSession, permission: schemas.PermissionCreate):
    db_permission = models.Permission(**permission.dict())
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

async def update_permission(db: AsyncSession, permission_id: int, permission: schemas.PermissionCreate):
    db_permission = await get_permission(db, permission_id)
    if db_permission:
        for key, value in permission.dict().items():
            setattr(db_permission, key, value)
        await db.commit()
        await db.refresh(db_permission)
    return db_permission

async def delete_permission(db: AsyncSession, permission_id: int):
    db_permission = await get_permission(db, permission_id)
    if db_permission:
        await db.delete(db_permission)
        await db.commit()
    return db_permission

# ---------------------------
# User CRUD
# ---------------------------
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.role))  # Preload role data
    )
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    user_data = user.dict()
    user_data.pop("password")  # Remove password to avoid duplicate arguments
    hashed_password = get_password_hash(user.password)
    
    db_user = models.User(**user_data, password=hashed_password)  # Now password is set correctly
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        try:
            await db.delete(db_user)
            await db.commit()
            return db_user
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            raise

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()

# ---------------------------
# Device CRUD
# ---------------------------
async def get_device(db: AsyncSession, device_id: int):
    result = await db.execute(
        select(models.Device)
        .options(joinedload(models.Device.organization))
        .where(models.Device.id == device_id)
    )
    device = result.scalars().first()
    return device

async def get_devices(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Device)
        .options(joinedload(models.Device.organization))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_device(db: AsyncSession, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def update_device(db: AsyncSession, device_id: int, device: schemas.DeviceCreate):
    db_device = await get_device(db, device_id)
    if db_device is None:
        return None
    for var, value in vars(device).items():
        setattr(db_device, var, value) if value else None
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def delete_device(db: AsyncSession, device_id: int):
    db_device = await get_device(db, device_id)
    if db_device is None:
        return None
    await db.delete(db_device)
    await db.commit()
    return db_device

# ---------------------------
# OrgDeviceMap CRUD
# ---------------------------
async def get_org_device_map(db: AsyncSession, map_id: int):
    result = await db.execute(select(models.OrgDeviceMap).where(models.OrgDeviceMap.id == map_id))
    return result.scalars().first()

async def get_org_device_maps(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.OrgDeviceMap).offset(skip).limit(limit))
    return result.scalars().all()

async def create_org_device_map(db: AsyncSession, org_device_map: schemas.OrgDeviceMapCreate):
    db_map = models.OrgDeviceMap(**org_device_map.dict())
    db.add(db_map)
    await db.commit()
    await db.refresh(db_map)
    return db_map

async def update_org_device_map(db: AsyncSession, map_id: int, org_device_map: schemas.OrgDeviceMapCreate):
    db_map = await get_org_device_map(db, map_id)
    if db_map:
        for key, value in org_device_map.dict().items():
            setattr(db_map, key, value)
        await db.commit()
        await db.refresh(db_map)
    return db_map

async def delete_org_device_map(db: AsyncSession, map_id: int):
    db_map = await get_org_device_map(db, map_id)
    if db_map:
        await db.delete(db_map)
        await db.commit()
    return db_map

# ---------------------------
# Reason CRUD
# ---------------------------
async def get_reasons(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Reason]:
    result = await db.execute(select(models.Reason).offset(skip).limit(limit))
    return result.scalars().all()

async def get_reasons_by_org_id(db: AsyncSession, org_id: int, skip: int = 0, limit: int = 100) -> List[models.Reason]:
    result = await db.execute(select(models.Reason).where(models.Reason.org_id == org_id).offset(skip).limit(limit))
    return result.scalars().all()

async def create_reason(db: AsyncSession, reason: schemas.ReasonCreate) -> models.Reason:
    db_reason = models.Reason(**reason.dict())
    db.add(db_reason)
    await db.commit()
    await db.refresh(db_reason)
    return db_reason

async def get_reason(db: AsyncSession, reason_id: int) -> models.Reason | None:
    result = await db.execute(select(models.Reason).filter(models.Reason.id == reason_id))
    return result.scalars().first()

async def update_reason(db: AsyncSession, reason_id: int, reason: schemas.ReasonCreate) -> models.Reason | None:
    db_reason = await get_reason(db, reason_id)
    if db_reason:
        for key, value in reason.dict().items():
            setattr(db_reason, key, value)
        await db.commit()
        await db.refresh(db_reason)
        return db_reason
    return None

async def delete_reason(db: AsyncSession, reason_id: int) -> models.Reason | None:
    db_reason = await get_reason(db, reason_id)
    if db_reason:
        await db.delete(db_reason)
        await db.commit()
        return db_reason
    return None

# ---------------------------
# DeviceLog CRUD
# ---------------------------
async def get_device_log(db: AsyncSession, log_id: int):
    result = await db.execute(select(models.DeviceLog).where(models.DeviceLog.id == log_id))
    return result.scalars().first()

async def get_device_logs(db: AsyncSession, skip: int = 0, limit: int = 100, device_id: Optional[int] = None):
    query = select(models.DeviceLog)
    if device_id is not None:
        query = query.where(models.DeviceLog.device_id == device_id)

    # Get total count
    count_query = select(func.count()).select_from(query)
    total = await db.execute(count_query)
    total = total.scalar()

    # Apply skip and limit for pagination
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()

    return logs, total

# ---------------------------
# DeviceReasonLog CRUD
# ---------------------------
async def get_device_reason_log(db: AsyncSession, log_id: int):
    result = await db.execute(select(models.DeviceReasonLog).where(models.DeviceReasonLog.id == log_id))
    return result.scalars().first()

async def get_device_reason_logs(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.DeviceReasonLog).offset(skip).limit(limit))
    return result.scalars().all()

async def create_device_reason_log(db: AsyncSession, log: schemas.DeviceReasonLogCreate):
    db_log = models.DeviceReasonLog(**log.dict())
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log

async def update_device_reason_log(db: AsyncSession, log_id: int, log: schemas.DeviceReasonLogCreate):
    db_log = await get_device_reason_log(db, log_id)
    if not db_log:
        return None
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    await db.commit()
    await db.refresh(db_log)
    return db_log

async def delete_device_reason_log(db: AsyncSession, log_id: int):
    db_log = await get_device_reason_log(db, log_id)
    if not db_log:
        return None
    await db.delete(db_log)
    await db.commit()
    return db_log
