from fastapi import FastAPI

from src.api.routers import tenant

app = FastAPI(title="CogniGraph")

app.include_router(tenant.router, tags=["Tenants"])
