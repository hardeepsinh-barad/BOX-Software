from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

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
    result = await db.execute(select(models.Organization).offset(skip).limit(limit))
    return result.scalars().all()

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
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
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
        await db.delete(db_user)
        await db.commit()
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()

# ---------------------------
# Device CRUD
# ---------------------------
async def get_device(db: AsyncSession, device_id: int):
    result = await db.execute(select(models.Device).where(models.Device.id == device_id))
    return result.scalars().first()

async def get_devices(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Device).offset(skip).limit(limit))
    return result.scalars().all()

async def create_device(db: AsyncSession, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def update_device(db: AsyncSession, device_id: int, device: schemas.DeviceCreate):
    db_device = await get_device(db, device_id)
    if db_device:
        for key, value in device.dict().items():
            setattr(db_device, key, value)
        await db.commit()
        await db.refresh(db_device)
    return db_device

async def delete_device(db: AsyncSession, device_id: int):
    db_device = await get_device(db, device_id)
    if db_device:
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
