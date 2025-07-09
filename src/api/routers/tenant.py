from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api import schemas
from src.core.services import tenant_service
from src.data.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tenants", response_model=schemas.Tenant, status_code=201)
def create_new_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.create_tenant(db=db, tenant=tenant)
