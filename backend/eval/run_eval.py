"""Retrieval hit-rate eval and MIN_SIMILARITY sweep. Run: python -m eval.run_eval"""
from app.config import settings
from app.db import close_pool, get_conn, open_pool
from app.services.embedder import embed
from app.services.retriever import search

# (user email, question, expected document title or None when nothing should be returned)
CASES = [
    ("employee@acme.example", "How many vacation days do I get?", "Acme Employee Handbook"),
    ("employee@acme.example", "When do I have to submit expense reports?", "Acme Employee Handbook"),
    ("employee@acme.example", "Which days am I expected in the office?", "Acme Employee Handbook"),
    ("manager@acme.example", "What is the Q4 sales quota increase?", "Acme Q4 Sales Plan"),
    ("manager@acme.example", "What is Project Falcon?", "Acme Q4 Sales Plan"),
    ("manager@acme.example", "Who approves discounts above 15%?", "Acme Q4 Sales Plan"),
    ("admin@acme.example", "What is the CEO's base salary?", "Acme CEO Compensation"),
    ("admin@acme.example", "What did the board decide about Brightwave?", "Acme Board Summary"),
    ("employee@globex.example", "How many days a week can I work remotely?", "Globex Employee Handbook"),
    ("manager@globex.example", "When does the Orion platform launch?", "Globex Product Roadmap"),
    ("admin@globex.example", "How big is the executive retention bonus?", "Globex Executive Compensation"),
    ("employee@acme.example", "What is the capital of France?", None),
    ("employee@acme.example", "How do I bake sourdough bread?", None),
]
THRESHOLDS = [0.0, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]


def evaluate(users, vectors, threshold):
    hits = answerable = abstain_ok = negatives = 0
    with get_conn() as conn:
        for (email, question, expected), vec in zip(CASES, vectors):
            u = users[email]
            results = search(conn, u["tenant_id"], u["role"], question, vec, threshold)
            titles = [r["title"] for r in results]
            if expected is None:
                negatives += 1
                abstain_ok += not titles
            else:
                answerable += 1
                hits += expected in titles
    return hits, answerable, abstain_ok, negatives


def main() -> None:
    open_pool()
    with get_conn() as conn:
        users = {r["email"]: r for r in conn.execute("SELECT email, tenant_id, role FROM users").fetchall()}
    vectors = embed([q for _, q, _ in CASES])
    print(f"{'MIN_SIMILARITY':<16}{'hit rate':<18}{'correct abstain'}")
    for t in THRESHOLDS:
        hits, answerable, ok, neg = evaluate(users, vectors, t)
        mark = "  <- current" if abs(t - settings.min_similarity) < 1e-9 else ""
        print(f"{t:<16.2f}{hits}/{answerable} ({100 * hits / answerable:.0f}%)".ljust(34) + f"{ok}/{neg}{mark}")
    close_pool()


if __name__ == "__main__":
    main()
