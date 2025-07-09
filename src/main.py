from fastapi import FastAPI

from src.api.routers import health, query, tenant

app = FastAPI(
    title="CogniGraph",
    description="A multi-tenant AI platform for querying private documents.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(tenant.router)
app.include_router(query.router)
