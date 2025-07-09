import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
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


@router.post("/tenants/{tenant_id}/upload", tags=["Documents"])
def upload_document_for_tenant(
    tenant_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    tenant = tenant_service.get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "tenant_id": tenant.id,
        "info": f"File saved to {temp_file_path}",
    }
