from sqlalchemy.orm import Session

from src.api.schemas import TenantCreate
from src.data.models import Tenant


def get_tenants(db: Session) -> list[Tenant]:
    return db.query(Tenant).all()


def create_tenant(db: Session, tenant: TenantCreate) -> Tenant:
    db_tenant = Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant
