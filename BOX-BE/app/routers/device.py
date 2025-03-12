from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=List[schemas.Device])
async def read_devices(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_devices(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Device)
async def create_device(device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_device(db, device)

@router.get("/{device_id}", response_model=schemas.Device)
async def read_device(device_id: int, db: AsyncSession = Depends(get_db)):
    db_device = await crud.get_device(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.put("/{device_id}", response_model=schemas.Device)
async def update_device(device_id: int, device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    db_device = await crud.update_device(db, device_id, device)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/{device_id}", response_model=schemas.Device)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    db_device = await crud.delete_device(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device