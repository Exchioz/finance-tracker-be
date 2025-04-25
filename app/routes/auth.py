from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils import hash_password, verify_password, create_access_token
from app.schemas import StandardResponse, UserCreate, UserLogin, UserResponse, LoginData
from app.database.session import get_db
from app.database.models.users import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create new User
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

# Login User
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