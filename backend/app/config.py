from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    @field_validator("jwt_secret")
    @classmethod
    def _validate_jwt_secret(cls, v: str) -> str:
        v = v.strip()
        placeholders = {
            "your-random-jwt-secret-here",
            "your-random-secret-key",
            "your-random-secret-key-at-least-32-chars-long",
            "change-me-generate-with-secrets-token-urlsafe",
        }
        if v in placeholders or "your-random" in v.lower() or "change-me" in v.lower():
            raise ValueError("JWT_SECRET must not be a placeholder from .env.example")
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return v
    jwt_expire_minutes: int = 480
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    max_upload_mb: int = 10
    min_similarity: float = 0.25
    min_keyword_similarity: float = 0.10
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
