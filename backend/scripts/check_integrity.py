"""Check integrity between chunks and parent documents. Run: python -m scripts.check_integrity"""
import sys

from app.db import close_pool, get_conn, open_pool


def check_integrity() -> bool:
    """Return True if all chunks match their parent documents, False otherwise."""
    with get_conn() as conn:
        orphaned = conn.execute(
            """SELECT c.id, c.document_id FROM chunks c
               LEFT JOIN documents d ON d.id = c.document_id
               WHERE d.id IS NULL"""
        ).fetchall()
        if orphaned:
            print(f"FAILED: Found {len(orphaned)} orphaned chunks with no parent document!")
            return False

        rows = conn.execute(
            """SELECT c.id AS chunk_id, c.document_id, c.tenant_id AS chunk_tenant, d.tenant_id AS doc_tenant,
                      c.allowed_roles AS chunk_roles, d.allowed_roles AS doc_roles
               FROM chunks c
               JOIN documents d ON d.id = c.document_id"""
        ).fetchall()

        mismatches = []
        for r in rows:
            if r["chunk_tenant"] != r["doc_tenant"]:
                mismatches.append(f"Chunk {r['chunk_id']}: tenant_id {r['chunk_tenant']} != doc {r['doc_tenant']}")
            elif sorted(r["chunk_roles"]) != sorted(r["doc_roles"]):
                mismatches.append(f"Chunk {r['chunk_id']}: roles {r['chunk_roles']} != doc {r['doc_roles']}")

        if mismatches:
            print(f"FAILED: Found {len(mismatches)} permission drift mismatches between chunks and parent docs:")
            for m in mismatches[:10]:
                print(f"  - {m}")
            return False

        print(f"PASS: Integrity verified across {len(rows)} chunks. All tenant_ids and allowed_roles match parent documents.")
        return True


def main() -> None:
    open_pool()
    try:
        ok = check_integrity()
        if not ok:
            sys.exit(1)
    finally:
        close_pool()


if __name__ == "__main__":
    main()
