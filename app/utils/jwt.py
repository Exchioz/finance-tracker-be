from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Union

from app.core.config import settings

def create_access_token(data: dict, expires_delta: Union[timedelta, None]=None):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire)
    )

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