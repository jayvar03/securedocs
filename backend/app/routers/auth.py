import psycopg
from fastapi import APIRouter, HTTPException

from app.db import get_conn
from app.schemas import LoginIn, RegisterTenantIn, TokenOut
from app.security import DUMMY_HASH, create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register-tenant", response_model=TokenOut, status_code=201)
def register_tenant(body: RegisterTenantIn):
    """Creates the company and its first admin in one transaction."""
    password_hash = hash_password(body.password)
    try:
        with get_conn() as conn:
            tenant = conn.execute(
                "INSERT INTO tenants (name) VALUES (%s) RETURNING id", (body.company_name,)
            ).fetchone()
            user = conn.execute(
                """INSERT INTO users (tenant_id, email, password_hash, role)
                   VALUES (%s, %s, %s, 'admin') RETURNING id""",
                (tenant["id"], body.email, password_hash),
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(409, "An account with this email already exists")

    user_out = {
        "id": user["id"],
        "tenant_id": tenant["id"],
        "email": body.email,
        "role": "admin",
        "department": None,
        "company_name": body.company_name,
    }
    return TokenOut(access_token=create_access_token(user["id"]), user=user_out)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn):
    with get_conn() as conn:
        user = conn.execute(
            """SELECT u.id, u.tenant_id, u.email, u.role, u.department, u.password_hash, t.name AS company_name
               FROM users u JOIN tenants t ON t.id = u.tenant_id
               WHERE u.email = %s""",
            (body.email,),
        ).fetchone()
    # Same work and same message for unknown user and wrong password.
    ok = verify_password(body.password, user["password_hash"] if user else DUMMY_HASH)
    if user is None or not ok:
        raise HTTPException(401, "Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})

    user_out = {
        "id": user["id"],
        "tenant_id": user["tenant_id"],
        "email": user["email"],
        "role": user["role"],
        "department": user["department"],
        "company_name": user["company_name"],
    }
    return TokenOut(access_token=create_access_token(user["id"]), user=user_out)

