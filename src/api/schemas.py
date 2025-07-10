import uuid
from datetime import datetime

from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str


class Tenant(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    query: str


class DocumentChunk(BaseModel):
    page_content: str
    metadata: dict

    class Config:
        from_attributes = True


class RetrievalResponse(BaseModel):
    retrieved_chunks: list[DocumentChunk]


class RagAnswer(BaseModel):
    answer: str
    sources: list[DocumentChunk]
