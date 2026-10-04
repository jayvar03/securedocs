"""Permission-aware hybrid retrieval (pgvector cosine search + full-text search + RRF)."""
import re

RRF_K = 60
CANDIDATES = 20
TOP_K = 5

_supports_iterative: bool | None = None


def build_tsquery(question: str, max_terms: int = 30) -> str:
    """Extract alphanumeric words from question and join with OR."""
    seen, words = set(), []
    for word in re.findall(r"[A-Za-z0-9]+", question.lower()):
        if word not in seen:
            seen.add(word)
            words.append(word)
    return " | ".join(words[:max_terms])


def rrf(rank_lists: list[list[int]], k: int = RRF_K) -> list[tuple[int, float]]:
    """Reciprocal Rank Fusion to merge ranked lists by position."""
    scores: dict[int, float] = {}
    for ranked in rank_lists:
        for position, item_id in enumerate(ranked, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + (1.0 / (k + position))
    return sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))


def _enable_iterative_scan(conn) -> None:
    global _supports_iterative
    if _supports_iterative is None:
        try:
            row = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
            major, minor = (int(x) for x in row["extversion"].split(".")[:2])
            _supports_iterative = (major, minor) >= (0, 8)
        except Exception:
            _supports_iterative = False

    if _supports_iterative:
        try:
            conn.execute("SET LOCAL hnsw.iterative_scan = relaxed_order")
        except Exception:
            pass



def _vector_search(conn, tenant_id: int, role: str, qvec, limit: int):
    _enable_iterative_scan(conn)
    return conn.execute(
        """WITH candidates AS MATERIALIZED (
               SELECT id, embedding <=> %(q)s AS distance
               FROM chunks
               WHERE tenant_id = %(tenant)s AND %(role)s = ANY(allowed_roles)
               ORDER BY embedding <=> %(q)s
               LIMIT %(limit)s
           )
           SELECT id, 1 - distance AS similarity FROM candidates ORDER BY distance + 0""",
        {"q": qvec, "tenant": tenant_id, "role": role, "limit": limit},
    ).fetchall()


def _text_search(conn, tenant_id: int, role: str, question: str, qvec, limit: int):
    tsq = build_tsquery(question)
    if not tsq:
        return []
    return conn.execute(
        """SELECT c.id, 1 - (c.embedding <=> %(q)s) AS similarity
           FROM chunks c, to_tsquery('english', %(tsq)s) AS query
           WHERE c.tenant_id = %(tenant)s 
             AND %(role)s = ANY(c.allowed_roles) 
             AND c.tsv @@ query
           ORDER BY ts_rank(c.tsv, query) DESC
           LIMIT %(limit)s""",
        {"tsq": tsq, "q": qvec, "tenant": tenant_id, "role": role, "limit": limit},
    ).fetchall()


def filter_and_fuse(
    vector_rows: list[dict],
    text_rows: list[dict],
    min_similarity: float,
    min_keyword_similarity: float,
    top_k: int = TOP_K,
) -> list[tuple[int, float]]:
    """Filter candidate rows by their respective similarity thresholds, then fuse with RRF."""
    vector_ids = [r["id"] for r in vector_rows if r["similarity"] >= min_similarity]
    text_ids = [r["id"] for r in text_rows if r["similarity"] >= min_keyword_similarity]
    return rrf([vector_ids, text_ids])[:top_k]


def search(
    conn,
    tenant_id: int,
    role: str,
    question: str,
    qvec,
    min_similarity: float,
    min_keyword_similarity: float = 0.10,
    top_k: int = TOP_K,
    candidates: int = CANDIDATES,
) -> list[dict]:
    # 1. Vector similarity search
    vector_rows = _vector_search(conn, tenant_id, role, qvec, candidates)

    # 2. Full-text keyword search (computes cosine similarity with qvec too)
    text_rows = _text_search(conn, tenant_id, role, question, qvec, candidates)

    # 3. Merge ranks with RRF after filtering by thresholds
    fused = filter_and_fuse(vector_rows, text_rows, min_similarity, min_keyword_similarity, top_k)
    if not fused:
        return []

    # 4. Fetch text content for winning chunk IDs
    winning_ids = [chunk_id for chunk_id, _ in fused]
    rows = conn.execute(
        """SELECT c.id, c.document_id, c.content, d.title
           FROM chunks c 
           JOIN documents d ON d.id = c.document_id
           WHERE c.id = ANY(%s) 
             AND c.tenant_id = %s 
             AND %s = ANY(c.allowed_roles)""",
        (winning_ids, tenant_id, role),
    ).fetchall()

    by_id = {r["id"]: r for r in rows}
    return [
        {
            "chunk_id": chunk_id,
            "document_id": by_id[chunk_id]["document_id"],
            "title": by_id[chunk_id]["title"],
            "content": by_id[chunk_id]["content"],
            "score": round(score, 4),
        }
        for chunk_id, score in fused
        if chunk_id in by_id
    ]


