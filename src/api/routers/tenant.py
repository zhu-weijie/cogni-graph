import os
import shutil
import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.deps import get_db
from src.celery_worker import celery_app, process_document_task
from src.core.services import tenant_service

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


@router.get("/")
def read_tenants(db: Session = Depends(get_db)):
    return tenant_service.get_tenants(db=db)


@router.post("/", status_code=201)
def create_new_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.create_tenant(db=db, tenant=tenant)


@router.post(
    "/{tenant_id}/upload",
    status_code=202,
    response_model=schemas.UploadResponse,
    tags=["Documents"],
)
def upload_document_for_tenant(
    tenant_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    tenant = tenant_service.get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    upload_dir = "/home/appuser/app/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = process_document_task.delay(
        file_path=file_path, tenant_id=str(tenant.id), doc_id=file.filename
    )

    return {"task_id": task.id, "status": "Processing"}


@router.get("/{tenant_id}/status/{task_id}", tags=["Documents"])
def get_task_status(tenant_id: uuid.UUID, task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }
    return response
