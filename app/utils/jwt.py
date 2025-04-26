from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    if settings.environment == "development":
        to_encode.update({"is_dev": True})
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    else:
        to_encode.update({"is_dev": False})
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.access_token_expire)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None