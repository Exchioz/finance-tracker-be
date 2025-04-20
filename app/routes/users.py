from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token, verify_access_token
from app.schemas.users import *
from app.schemas.responses import StandardResponse
from app.database.session import get_db
from app.database.models.users import User

router = APIRouter()
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

@router.post("/register", response_model=StandardResponse)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return StandardResponse(
        message="User registered successfully",
        data=UserResponse.from_orm(new_user)
    )

@router.post("/login", response_model=StandardResponse)
async def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(db_user.id)})

    return StandardResponse(
        message="Login successful",
        data=LoginData(access_token=token)
    )

@router.get("/me", response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)