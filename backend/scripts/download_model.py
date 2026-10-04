"""Download the embedding model into .model_cache (run at build time so cold starts are fast).
Run: python -m scripts.download_model"""
from app.services.embedder import CACHE_DIR, embed


def main() -> None:
    vectors = embed(["warm up"])
    print(f"Model ready in {CACHE_DIR}, vector shape {vectors.shape}")


if __name__ == "__main__":
    main()
