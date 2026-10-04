from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.routers.users import delete_user, update_user
from app.schemas import UserUpdateIn


def test_user_update_schema_rejects_extra_fields():
    with pytest.raises(ValidationError):
        UserUpdateIn(role="employee", tenant_id=1)
    with pytest.raises(ValidationError):
        UserUpdateIn(email="hack@example.com")
    valid = UserUpdateIn(role="manager", department="Sales")
    assert valid.role == "manager"
    assert valid.department == "Sales"


def test_self_demotion_rejected():
    mock_conn = MagicMock()
    # Target is self (id=1, admin)
    mock_conn.execute.return_value.fetchone.return_value = {
        "id": 1,
        "tenant_id": 10,
        "email": "admin@example.com",
        "role": "admin",
        "department": "Exec",
    }
    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}
        with pytest.raises(HTTPException) as exc:
            update_user(user_id=1, body=UserUpdateIn(role="employee"), admin=admin)
        assert exc.value.status_code == 400
        assert "cannot demote yourself" in exc.value.detail.lower()


def test_last_admin_demotion_rejected():
    mock_conn = MagicMock()
    # Target is admin 2, caller is admin 1, but total admins count is 1
    mock_conn.execute.return_value.fetchone.side_effect = [
        {"id": 2, "tenant_id": 10, "email": "other@example.com", "role": "admin", "department": None},
        {"c": 1},  # count of admins is 1
    ]
    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}
        with pytest.raises(HTTPException) as exc:
            update_user(user_id=2, body=UserUpdateIn(role="employee"), admin=admin)
        assert exc.value.status_code == 400
        assert "last admin" in exc.value.detail.lower()


def test_self_deletion_rejected():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = {
        "id": 1,
        "tenant_id": 10,
        "email": "admin@example.com",
        "role": "admin",
        "department": "Exec",
    }
    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}
        with pytest.raises(HTTPException) as exc:
            delete_user(user_id=1, admin=admin)
        assert exc.value.status_code == 400
        assert "cannot delete your own account" in exc.value.detail.lower()


def test_last_admin_deletion_rejected():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.side_effect = [
        {"id": 2, "tenant_id": 10, "email": "other@example.com", "role": "admin", "department": None},
        {"c": 1},  # count of admins is 1
    ]
    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}
        with pytest.raises(HTTPException) as exc:
            delete_user(user_id=2, admin=admin)
        assert exc.value.status_code == 400
        assert "last admin" in exc.value.detail.lower()


def test_user_not_found_or_different_tenant():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = None
    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}
        with pytest.raises(HTTPException) as exc:
            delete_user(user_id=999, admin=admin)
        assert exc.value.status_code == 404
