import os

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.config import settings
from app.db import get_conn
from app.deps import get_current_user, require_role
from app.roles import normalize_roles
from app.schemas import AccessIn, DocumentOut
from app.services.extract import (
    ALLOWED_EXTENSIONS,
    EmptyDocument,
    ExtractionError,
    extract_text,
)
from app.services.ingest import ingest_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

DOC_COLUMNS = "id, title, filename, allowed_roles, uploaded_by, created_at"


@router.post("", response_model=DocumentOut, status_code=201)
def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    allowed_roles: list[str] = Form(default=[]),
    user: dict = Depends(require_role("admin", "manager")),
):
    filename = file.filename or ""
    # Cheap checks first: extension (415), size (413), roles (422), then extract/embed.
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(415, "Unsupported file type. Upload a PDF, TXT or MD file.")

    max_bytes = settings.max_upload_mb * 1024 * 1024
    data = file.file.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise HTTPException(413, f"File is too large. The limit is {settings.max_upload_mb} MB.")

    try:
        roles = normalize_roles(allowed_roles)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    try:
        text = extract_text(filename, data)
    except (EmptyDocument, ExtractionError) as exc:
        raise HTTPException(422, str(exc))

    clean_title = (title or "").strip() or os.path.splitext(filename)[0]
    return ingest_document(
        tenant_id=user["tenant_id"],  # from the logged-in user, never the request
        uploaded_by=user["id"],
        title=clean_title[:200],
        filename=filename[:255],
        allowed_roles=roles,
        text=text,
    )


@router.get("", response_model=list[DocumentOut])
def list_documents(user: dict = Depends(get_current_user)):
    with get_conn() as conn:
        return conn.execute(
            f"""SELECT {DOC_COLUMNS} FROM documents
                WHERE tenant_id = %s AND %s = ANY(allowed_roles)
                ORDER BY created_at DESC, id DESC""",
            (user["tenant_id"], user["role"]),
        ).fetchall()


@router.patch("/{document_id}/access", response_model=DocumentOut)
def change_access(document_id: int, body: AccessIn, admin: dict = Depends(require_role("admin"))):
    roles = normalize_roles(list(body.allowed_roles))  # admin is always kept
    with get_conn() as conn:  # one transaction: document and ALL its chunks change together
        doc = conn.execute(
            f"""UPDATE documents SET allowed_roles = %s
                WHERE id = %s AND tenant_id = %s RETURNING {DOC_COLUMNS}""",
            (roles, document_id, admin["tenant_id"]),
        ).fetchone()
        if doc is None:
            raise HTTPException(404, "Document not found")
        conn.execute(
            "UPDATE chunks SET allowed_roles = %s WHERE document_id = %s AND tenant_id = %s",
            (roles, document_id, admin["tenant_id"]),
        )
    return doc


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, admin: dict = Depends(require_role("admin"))):
    with get_conn() as conn:
        deleted = conn.execute(
            "DELETE FROM documents WHERE id = %s AND tenant_id = %s RETURNING id",
            (document_id, admin["tenant_id"]),
        ).fetchone()  # chunks go with it (ON DELETE CASCADE)
    if deleted is None:
        raise HTTPException(404, "Document not found")
