from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from app import schemas, crud
from app.database import get_db
from pydantic import BaseModel

class DeviceLogList(BaseModel):
    logs: List[schemas.DeviceLog]
    total: int

router = APIRouter(prefix="/device_logs", tags=["device_logs"])

@router.get("/", response_model=DeviceLogList)
async def read_device_logs(
    skip: int = 0,
    limit: int = 100,
    device_id: Optional[int] = Query(None, description="Filter by device ID"),
    db: AsyncSession = Depends(get_db)
) -> DeviceLogList:
    logs, total = await crud.get_device_logs(db, skip=skip, limit=limit, device_id=device_id)
    # Convert models to schemas
    schema_logs = [schemas.DeviceLog.from_orm(log) for log in logs]
    return DeviceLogList(logs=schema_logs, total=total)

@router.post("/", response_model=schemas.DeviceLog)
async def create_device_log(log: schemas.DeviceLogCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_device_log(db, log)

@router.get("/{log_id}", response_model=schemas.DeviceLog)
async def read_device_log(log_id: int, db: AsyncSession = Depends(get_db)):
    db_log = await crud.get_device_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceLog not found")
    return db_log

@router.put("/{log_id}", response_model=schemas.DeviceLog)
async def update_device_log(log_id: int, log: schemas.DeviceLogCreate, db: AsyncSession = Depends(get_db)):
    db_log = await crud.update_device_log(db, log_id, log)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceLog not found")
    return db_log

@router.delete("/{log_id}", response_model=schemas.DeviceLog)
async def delete_device_log(log_id: int, db: AsyncSession = Depends(get_db)):
    db_log = await crud.delete_device_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="DeviceLog not found")
    return db_log
