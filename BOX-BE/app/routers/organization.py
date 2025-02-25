from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas, crud
from app.database import get_db  # Your dependency that yields an AsyncSession

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.get("/", response_model=List[schemas.Organization])
async def read_organizations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Organization)
async def create_organization(organization: schemas.OrganizationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_organization(db, organization)

@router.get("/{org_id}", response_model=schemas.Organization)
async def read_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    db_org = await crud.get_organization(db, org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.put("/{org_id}", response_model=schemas.Organization)
async def update_organization(org_id: int, organization: schemas.OrganizationCreate, db: AsyncSession = Depends(get_db)):
    db_org = await crud.update_organization(db, org_id, organization)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.delete("/{org_id}", response_model=schemas.Organization)
async def delete_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    db_org = await crud.delete_organization(db, org_id)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org
