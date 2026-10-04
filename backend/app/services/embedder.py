"""Vector embeddings with fastembed (all-MiniLM-L6-v2, 384 dimensions)."""
import os
from pathlib import Path
import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSIONS = 384
CACHE_DIR = os.environ.get("MODEL_CACHE_DIR", str(Path(__file__).resolve().parents[2] / ".model_cache"))

_model: TextEmbedding | None = None


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=MODEL_NAME, cache_dir=CACHE_DIR)
    return _model


def embed(texts: list[str]) -> np.ndarray:
    """Return an (N, 384) float32 array of normalized vectors."""
    return np.array(list(get_model().embed(texts)), dtype=np.float32)


def embed_one(text: str) -> np.ndarray:
    return embed([text])[0]


