import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


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


class AgentResponse(BaseModel):
    output: str
    intermediate_steps: list[Any] = Field(default_factory=list)


class UploadResponse(BaseModel):
    task_id: str
    status: str
