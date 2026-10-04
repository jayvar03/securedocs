from app.db import get_conn
from app.services.chunker import chunk_text
from app.services.embedder import embed


def ingest_document(*, tenant_id: int, uploaded_by: int | None, title: str, filename: str,
                    allowed_roles: list[str], text: str) -> dict:
    """Chunk -> embed (before touching the DB) -> store document + chunks in ONE transaction."""
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError("Document has no text")
    vectors = embed(chunks)  # slow work happens before we hold a DB connection

    with get_conn() as conn:
        doc = conn.execute(
            """INSERT INTO documents (tenant_id, title, filename, allowed_roles, uploaded_by)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING id, title, filename, allowed_roles, uploaded_by, created_at""",
            (tenant_id, title, filename, allowed_roles, uploaded_by),
        ).fetchone()
        with conn.cursor() as cur:
            cur.executemany(
                """INSERT INTO chunks (document_id, tenant_id, allowed_roles, chunk_index, content, embedding)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                [
                    # tenant_id and allowed_roles are copied from the document onto every chunk
                    (doc["id"], tenant_id, allowed_roles, i, content, vector)
                    for i, (content, vector) in enumerate(zip(chunks, vectors))
                ],
            )
    doc["chunk_count"] = len(chunks)
    return doc
