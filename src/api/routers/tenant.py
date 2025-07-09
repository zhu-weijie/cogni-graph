from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.deps import get_db
from src.core.services import tenant_service

router = APIRouter()


@router.get("/tenants", response_model=List[schemas.Tenant])
def read_tenants(db: Session = Depends(get_db)):
    return tenant_service.get_tenants(db=db)


@router.post("/tenants", response_model=schemas.Tenant, status_code=201)
def create_new_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.create_tenant(db=db, tenant=tenant)
