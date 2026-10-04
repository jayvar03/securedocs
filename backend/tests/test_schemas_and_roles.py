import pytest
from pydantic import ValidationError

from app.roles import normalize_roles
from app.schemas import UserCreateIn


def test_admin_always_added_and_empty_means_admin_only():
    assert normalize_roles([]) == ["admin"]
    assert normalize_roles(["employee"]) == ["admin", "employee"]
    assert normalize_roles(["manager,employee", "manager"]) == ["admin", "manager", "employee"]


def test_unknown_role_rejected():
    with pytest.raises(ValueError):
        normalize_roles(["root"])


def test_create_user_rejects_tenant_id():
    with pytest.raises(ValidationError):
        UserCreateIn(email="a@b.co", password="longenough", role="employee", tenant_id=5)


def test_password_limits():
    with pytest.raises(ValidationError):
        UserCreateIn(email="a@b.co", password="short", role="employee")
    with pytest.raises(ValidationError):
        UserCreateIn(email="a@b.co", password="x" * 73, role="employee")


def test_jwt_secret_validation():
    from app.config import Settings
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://fake", jwt_secret="short-key")
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://fake", jwt_secret="your-random-jwt-secret-here")
    valid = Settings(database_url="postgresql://fake", jwt_secret="0123456789abcdef0123456789abcdef")
    assert valid.jwt_secret == "0123456789abcdef0123456789abcdef"

