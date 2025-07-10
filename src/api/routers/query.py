import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.deps import get_db
from src.core.services import document_service, qa_service, tenant_service

router = APIRouter(
    prefix="/tenants/{tenant_id}/query",
    tags=["Query"],
)


@router.post("/retrieve", response_model=schemas.RetrievalResponse)
def retrieve_documents_for_query(
    tenant_id: uuid.UUID, request: schemas.QueryRequest, db: Session = Depends(get_db)
):
    tenant = tenant_service.get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    retrieved_chunks = document_service.search_documents(
        query=request.query, tenant_id=str(tenant.id)
    )

    return {"retrieved_chunks": retrieved_chunks}


@router.post("/{tenant_id}/query/generate", response_model=str)
def generate_answer_from_query(
    tenant_id: uuid.UUID, request: schemas.QueryRequest, db: Session = Depends(get_db)
):
    tenant = tenant_service.get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    retrieved_chunks = document_service.search_documents(
        query=request.query, tenant_id=str(tenant.id)
    )

    answer = qa_service.generate_answer(query=request.query, context=retrieved_chunks)

    return answer
