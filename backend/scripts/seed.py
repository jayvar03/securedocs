"""Create two demo companies with users and documents.

Run: python -m scripts.seed          (skips companies that already exist)
     python -m scripts.seed --reset  (deletes the demo companies first)
"""
import sys

from app.db import close_pool, get_conn, open_pool
from app.security import hash_password
from app.services.ingest import ingest_document
from scripts.seed_data import DEMO_PASSWORD, TENANTS


def main(reset: bool) -> None:
    open_pool()
    password_hash = hash_password(DEMO_PASSWORD)
    for tenant in TENANTS:
        with get_conn() as conn:
            existing = conn.execute("SELECT id FROM tenants WHERE name = %s", (tenant["name"],)).fetchone()
            if existing and reset:
                conn.execute("DELETE FROM tenants WHERE id = %s", (existing["id"],))
                existing = None
            if existing:
                print(f"{tenant['name']}: already exists, skipping (use --reset to recreate)")
                continue
            tenant_id = conn.execute(
                "INSERT INTO tenants (name) VALUES (%s) RETURNING id", (tenant["name"],)
            ).fetchone()["id"]
            admin_id = None
            for email, role, department in tenant["users"]:
                uid = conn.execute(
                    """INSERT INTO users (tenant_id, email, password_hash, role, department)
                       VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    (tenant_id, email, password_hash, role, department),
                ).fetchone()["id"]
                if role == "admin":
                    admin_id = uid
        for doc in tenant["docs"]:
            result = ingest_document(
                tenant_id=tenant_id, uploaded_by=admin_id, title=doc["title"],
                filename=doc["filename"], allowed_roles=doc["roles"], text=doc["text"],
            )
            print(f"  {tenant['name']}: {doc['title']} ({result['chunk_count']} chunks, roles={doc['roles']})")
    close_pool()
    print(f"Done. Demo password for every seeded user: {DEMO_PASSWORD}")


if __name__ == "__main__":
    main(reset="--reset" in sys.argv)
