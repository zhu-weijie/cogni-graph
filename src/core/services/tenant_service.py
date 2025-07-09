import uuid

from sqlalchemy.orm import Session

from src.api.schemas import TenantCreate
from src.data.models import Tenant


def get_tenants(db: Session) -> list[Tenant]:
    return db.query(Tenant).all()


def get_tenant_by_id(db: Session, tenant_id: uuid.UUID) -> Tenant | None:
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def create_tenant(db: Session, tenant: TenantCreate) -> Tenant:
    db_tenant = Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant
