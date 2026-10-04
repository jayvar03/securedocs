import time
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db import get_conn
from app.security import decode_access_token

bearer = HTTPBearer(auto_error=False)

# Short in-memory cache so page navigation doesn't make redundant database round-trips
_USER_CACHE: dict[int, tuple[dict, float]] = {}
USER_CACHE_TTL = 30.0  # seconds


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    if creds is None:
        raise HTTPException(401, "Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    user_id = decode_access_token(creds.credentials)
    if user_id is None:
        raise HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    now = time.time()
    cached = _USER_CACHE.get(user_id)
    if cached and (now - cached[1]) < USER_CACHE_TTL:
        return cached[0]

    with get_conn() as conn:
        user = conn.execute(
            """SELECT u.id, u.tenant_id, u.email, u.role, u.department, t.name AS company_name
               FROM users u JOIN tenants t ON t.id = u.tenant_id
               WHERE u.id = %s""",
            (user_id,),
        ).fetchone()
    if user is None:
        raise HTTPException(401, "Account no longer exists", headers={"WWW-Authenticate": "Bearer"})

    _USER_CACHE[user_id] = (user, now)
    return user



def require_role(*roles: str):
    def checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(403, "You do not have permission to do this")
        return user

    return checker
