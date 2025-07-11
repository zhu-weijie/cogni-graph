from unittest.mock import Mock

from src.api.schemas import TenantCreate
from src.core.services import tenant_service


def test_create_tenant():
    mock_db_session = Mock()

    tenant_create_data = TenantCreate(name="Test Tenant")

    tenant_service.create_tenant(db=mock_db_session, tenant=tenant_create_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
