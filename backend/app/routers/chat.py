from fastapi import APIRouter, Depends, HTTPException, Request

from app.config import settings
from app.db import get_conn
from app.deps import get_current_user
from app.limiter import limiter
from app.schemas import ChatIn, ChatOut
from app.services.embedder import embed_one
from app.services.llm import NOT_FOUND, LLMError, generate_answer
from app.services.retriever import search

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatOut)
@limiter.limit("20/minute")
def chat(request: Request, body: ChatIn, user: dict = Depends(get_current_user)):
    qvec = embed_one(body.question)  # before opening a DB connection

    with get_conn() as conn:
        passages = search(conn, user["tenant_id"], user["role"], body.question, qvec,
                          settings.min_similarity)
        conn.execute(
            "INSERT INTO audit_logs (tenant_id, user_id, question, chunk_ids) VALUES (%s, %s, %s, %s)",
            (user["tenant_id"], user["id"], body.question, [p["chunk_id"] for p in passages]),
        )

    if not passages:
        # Nothing allowed and relevant: skip the LLM (no cost, no hallucination, no leak).
        return ChatOut(answer=NOT_FOUND, sources=[], found=False)

    try:
        answer = generate_answer(body.question, passages)
    except LLMError:
        raise HTTPException(500, "The answer service is unavailable. Please try again.")

    # Sources keep the same order as the [1], [2] citations in the prompt.
    sources = [{"title": p["title"], "chunk_id": p["chunk_id"], "score": p["score"]} for p in passages]
    return ChatOut(answer=answer, sources=sources, found=True)
