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
    # fetchone returns target user; fetchall returns locked admin rows for tenant (only 1 admin)
    mock_conn.execute.return_value.fetchone.return_value = {
        "id": 2, "tenant_id": 10, "email": "other@example.com", "role": "admin", "department": None
    }
    mock_conn.execute.return_value.fetchall.return_value = [{"id": 2}]
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
    mock_conn.execute.return_value.fetchone.return_value = {
        "id": 2, "tenant_id": 10, "email": "other@example.com", "role": "admin", "department": None
    }
    # fetchall returns locked admin rows (only 1 admin remaining)
    mock_conn.execute.return_value.fetchall.return_value = [{"id": 2}]
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


def test_update_user_department_clearing_vs_omitted():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.side_effect = [
        # Target user currently in "Sales"
        {"id": 2, "tenant_id": 10, "email": "user2@example.com", "role": "employee", "department": "Sales"},
        # Updated user return row
        {"id": 2, "tenant_id": 10, "email": "user2@example.com", "role": "employee", "department": None},
    ]

    with patch("app.routers.users.get_conn") as mock_get_conn:
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        admin = {"id": 1, "tenant_id": 10, "role": "admin"}

        # 1. Explicitly sending department: None clears it
        body_clear = UserUpdateIn.model_validate({"department": None})
        update_user(user_id=2, body=body_clear, admin=admin)

        # Check what was passed to UPDATE
        update_sql, update_params = mock_conn.execute.call_args_list[-1][0]
        assert "UPDATE users" in update_sql
        # update_params: (new_role, new_dept, user_id, tenant_id)
        assert update_params[1] is None

        # 2. Omitted department keeps existing department ("Sales")
        mock_conn.execute.return_value.fetchone.side_effect = [
            {"id": 2, "tenant_id": 10, "email": "user2@example.com", "role": "employee", "department": "Sales"},
            {"id": 2, "tenant_id": 10, "email": "user2@example.com", "role": "manager", "department": "Sales"},
        ]
        body_omit = UserUpdateIn.model_validate({"role": "manager"})
        update_user(user_id=2, body=body_omit, admin=admin)
        update_sql, update_params = mock_conn.execute.call_args_list[-1][0]
        assert update_params[1] == "Sales"
