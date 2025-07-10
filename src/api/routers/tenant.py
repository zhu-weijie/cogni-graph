import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from neo4j import Session as Neo4jSession
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.deps import get_db, get_graph_session
from src.core.services import document_service, tenant_service

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


@router.post("/{tenant_id}/upload", tags=["Documents"])
def upload_document_for_tenant(
    tenant_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    graph_db: Neo4jSession = Depends(get_graph_session),
):
    tenant = tenant_service.get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    num_chunks, num_nodes, num_rels = document_service.process_document(
        file_path=temp_file_path,
        tenant_id=str(tenant.id),
        doc_id=file.filename,
        neo4j_session=graph_db,
    )

    return {
        "filename": file.filename,
        "tenant_id": tenant.id,
        "rag_chunks_stored": num_chunks,
        "kg_nodes_created": num_nodes,
        "kg_relationships_created": num_rels,
    }
