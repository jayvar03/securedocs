import psycopg
from fastapi import APIRouter, Depends, HTTPException, Response

from app.db import get_conn
from app.deps import get_current_user, require_role
from app.schemas import UserCreateIn, UserOut, UserUpdateIn
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


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, body: UserUpdateIn, admin: dict = Depends(require_role("admin"))):
    with get_conn() as conn:
        target = conn.execute(
            """SELECT id, tenant_id, email, role, department
               FROM users WHERE id = %s AND tenant_id = %s""",
            (user_id, admin["tenant_id"]),
        ).fetchone()
        if target is None:
            raise HTTPException(404, "User not found")

        if "role" in body.model_fields_set and body.role is not None and body.role != target["role"]:
            if target["id"] == admin["id"]:
                raise HTTPException(400, "You cannot demote yourself from admin")
            if target["role"] == "admin":
                admin_rows = conn.execute(
                    "SELECT id FROM users WHERE tenant_id = %s AND role = 'admin' FOR UPDATE",
                    (admin["tenant_id"],),
                ).fetchall()
                if len(admin_rows) <= 1:
                    raise HTTPException(400, "Cannot remove or demote the last admin of a tenant")

        new_role = body.role if ("role" in body.model_fields_set and body.role is not None) else target["role"]
        if "department" in body.model_fields_set:
            new_dept = (body.department.strip() or None) if body.department else None
        else:
            new_dept = target["department"]

        row = conn.execute(
            """UPDATE users SET role = %s, department = %s
               WHERE id = %s AND tenant_id = %s
               RETURNING id, tenant_id, email, role, department""",
            (new_role, new_dept, user_id, admin["tenant_id"]),
        ).fetchone()
        return row


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, admin: dict = Depends(require_role("admin"))):
    with get_conn() as conn:
        target = conn.execute(
            """SELECT id, tenant_id, email, role, department
               FROM users WHERE id = %s AND tenant_id = %s""",
            (user_id, admin["tenant_id"]),
        ).fetchone()
        if target is None:
            raise HTTPException(404, "User not found")

        if target["id"] == admin["id"]:
            raise HTTPException(400, "You cannot delete your own account")

        if target["role"] == "admin":
            admin_rows = conn.execute(
                "SELECT id FROM users WHERE tenant_id = %s AND role = 'admin' FOR UPDATE",
                (admin["tenant_id"],),
            ).fetchall()
            if len(admin_rows) <= 1:
                raise HTTPException(400, "Cannot remove the last admin of a tenant")

        conn.execute(
            "DELETE FROM users WHERE id = %s AND tenant_id = %s",
            (user_id, admin["tenant_id"]),
        )
    return Response(status_code=204)
