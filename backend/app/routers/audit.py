from fastapi import APIRouter, Depends

from app.db import get_conn
from app.deps import require_role
from app.schemas import AuditOut

router = APIRouter(prefix="/api/audit-logs", tags=["audit"])


@router.get("", response_model=list[AuditOut])
def list_audit_logs(admin: dict = Depends(require_role("admin"))):
    with get_conn() as conn:
        return conn.execute(
            """SELECT a.id, a.user_id, u.email AS user_email, a.question, a.chunk_ids, a.created_at
               FROM audit_logs a LEFT JOIN users u ON u.id = a.user_id
               WHERE a.tenant_id = %s
               ORDER BY a.created_at DESC, a.id DESC LIMIT 200""",
            (admin["tenant_id"],),
        ).fetchall()
