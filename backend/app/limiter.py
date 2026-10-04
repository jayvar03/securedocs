from slowapi import Limiter
from slowapi.util import get_remote_address

from app.security import decode_access_token


def user_key(request) -> str:
    """Rate-limit per user when a valid token is present, otherwise per IP."""
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        user_id = decode_access_token(auth[7:].strip())
        if user_id is not None:
            return f"user:{user_id}"
    return get_remote_address(request)


limiter = Limiter(key_func=user_key)
