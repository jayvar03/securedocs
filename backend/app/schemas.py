import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Role = Literal["admin", "manager", "employee"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean_email(value: str) -> str:
    value = value.strip().lower()
    if len(value) > 254 or not EMAIL_RE.match(value):
        raise ValueError("Enter a valid email address")
    return value


def _check_password(value: str) -> str:
    if len(value.encode("utf-8")) > 72:  # bcrypt limit is in bytes
        raise ValueError("Password must be at most 72 bytes")
    return value


class RegisterTenantIn(BaseModel):
    company_name: str = Field(min_length=1, max_length=100)
    email: str
    password: str = Field(min_length=8, max_length=72)

    _email = field_validator("email")(_clean_email)
    _password = field_validator("password")(_check_password)

    @field_validator("company_name")
    @classmethod
    def _name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Company name is required")
        return v


class LoginIn(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        return v.strip().lower()


class UserCreateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")  # a sent tenant_id gives 422

    email: str
    password: str = Field(min_length=8, max_length=72)
    role: Role
    department: str | None = Field(default=None, max_length=100)

    _email = field_validator("email")(_clean_email)
    _password = field_validator("password")(_check_password)


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: str
    role: Role
    department: str | None = None
    company_name: str | None = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut | None = None



class DocumentOut(BaseModel):
    id: int
    title: str
    filename: str
    allowed_roles: list[str]
    uploaded_by: int | None = None
    created_at: datetime
    chunk_count: int | None = None


class AccessIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    allowed_roles: list[Role]


class ChatIn(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def _q(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question is required")
        return v


class SourceOut(BaseModel):
    title: str
    chunk_id: int
    score: float


class ChatOut(BaseModel):
    answer: str
    sources: list[SourceOut]
    found: bool


class AuditOut(BaseModel):
    id: int
    user_id: int | None
    user_email: str | None
    question: str
    chunk_ids: list[int]
    created_at: datetime
