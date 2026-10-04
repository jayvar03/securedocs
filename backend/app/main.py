import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.db import close_pool, open_pool
from app.limiter import limiter
from app.routers import audit, auth, chat, documents, users
from app.services.embedder import get_model

log = logging.getLogger("securedocs")


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_pool()
    get_model()  # warm up the embedder so the first request is not slow
    yield
    close_pool()


app = FastAPI(title="SecureDocs", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limited(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        {"detail": "Too many questions. Please wait a minute and try again."},
        status_code=429,
        headers={"Retry-After": "60"},
    )


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse({"detail": "Something went wrong on the server."}, status_code=500)


for module in (auth, users, documents, chat, audit):
    app.include_router(module.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
