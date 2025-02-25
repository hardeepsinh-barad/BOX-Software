from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/reasons", tags=["reasons"])

@router.get("/", response_model=List[schemas.Reason])
async def read_reasons(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_reasons(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Reason)
async def create_reason(reason: schemas.ReasonCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_reason(db, reason)

@router.get("/{reason_id}", response_model=schemas.Reason)
async def read_reason(reason_id: int, db: AsyncSession = Depends(get_db)):
    db_reason = await crud.get_reason(db, reason_id)
    if not db_reason:
        raise HTTPException(status_code=404, detail="Reason not found")
    return db_reason

@router.put("/{reason_id}", response_model=schemas.Reason)
async def update_reason(reason_id: int, reason: schemas.ReasonCreate, db: AsyncSession = Depends(get_db)):
    db_reason = await crud.update_reason(db, reason_id, reason)
    if not db_reason:
        raise HTTPException(status_code=404, detail="Reason not found")
    return db_reason

@router.delete("/{reason_id}", response_model=schemas.Reason)
async def delete_reason(reason_id: int, db: AsyncSession = Depends(get_db)):
    db_reason = await crud.delete_reason(db, reason_id)
    if not db_reason:
        raise HTTPException(status_code=404, detail="Reason not found")
    return db_reason
