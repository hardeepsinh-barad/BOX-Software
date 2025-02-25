from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/device_reason_logs", tags=["device_reason_logs"])

@router.get("/", response_model=List[schemas.DeviceReasonLog])
async def read_device_reason_logs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_device_reason_logs(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.DeviceReasonLog)
async def create_device_reason_log(log: schemas.DeviceReasonLogCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_device_reason_log(db, log)

@router.get("/{log_id}", response_model=schemas.DeviceReasonLog)
async def read_device_reason_log(log_id: int, db: AsyncSession = Depends(get_db)):
    db_log = await crud.get_device_reason_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceReasonLog not found")
    return db_log

@router.put("/{log_id}", response_model=schemas.DeviceReasonLog)
async def update_device_reason_log(log_id: int, log: schemas.DeviceReasonLogCreate, db: AsyncSession = Depends(get_db)):
    db_log = await crud.update_device_reason_log(db, log_id, log)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceReasonLog not found")
    return db_log

@router.delete("/{log_id}", response_model=schemas.DeviceReasonLog)
async def delete_device_reason_log(log_id: int, db: AsyncSession = Depends(get_db)):
    db_log = await crud.delete_device_reason_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceReasonLog not found")
    return db_log
