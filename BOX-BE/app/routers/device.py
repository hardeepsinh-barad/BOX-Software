from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, crud
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=List[schemas.Device])
async def read_devices(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        devices = await crud.get_devices(db, skip=skip, limit=limit)
        for device in devices:
            if device.organization:
                device.organization_name = device.organization.name
        return devices
    except Exception as e:
        logger.error(f"Error reading devices: {e}")
        raise HTTPException(status_code=500, detail="Failed to read devices")

@router.post("/", response_model=schemas.Device)
async def create_device(device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_device(db, device)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Failed to create device")

@router.get("/{device_id}", response_model=schemas.Device)
async def read_device(device_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_device = await crud.get_device(db, device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found")

        # Directly access the organization name from the preloaded relationship
        if db_device.organization:
            db_device.organization_name = db_device.organization.name

        return db_device
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"Error reading device: {e}")
        raise HTTPException(status_code=500, detail="Failed to read device")

@router.put("/{device_id}", response_model=schemas.Device)
async def update_device(device_id: int, device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_device = await crud.update_device(db, device_id, device)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found")
        return db_device
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        raise HTTPException(status_code=500, detail="Failed to update device")

@router.delete("/{device_id}", response_model=schemas.Device)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_device = await crud.delete_device(db, device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found")
        return db_device
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete device")