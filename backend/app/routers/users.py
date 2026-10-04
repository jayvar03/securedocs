import psycopg
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_conn
from app.deps import get_current_user, require_role
from app.schemas import UserCreateIn, UserOut
from app.security import hash_password

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return user


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreateIn, admin: dict = Depends(require_role("admin"))):
    password_hash = hash_password(body.password)
    try:
        with get_conn() as conn:
            row = conn.execute(
                """INSERT INTO users (tenant_id, email, password_hash, role, department)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id, tenant_id, email, role, department""",
                # tenant_id ALWAYS comes from the logged-in admin
                (admin["tenant_id"], body.email, password_hash, body.role, body.department),
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(409, "A user with this email already exists")
    return row


@router.get("", response_model=list[UserOut])
def list_users(admin: dict = Depends(require_role("admin"))):
    with get_conn() as conn:
        return conn.execute(
            """SELECT id, tenant_id, email, role, department
               FROM users WHERE tenant_id = %s ORDER BY created_at, id""",
            (admin["tenant_id"],),
        ).fetchall()
