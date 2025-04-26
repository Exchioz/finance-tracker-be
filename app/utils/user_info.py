from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.jwt import verify_access_token
from app.database.session import get_db
from app.database.models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    try:
        user = db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user