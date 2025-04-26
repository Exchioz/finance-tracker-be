from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas import *
from app.database.models import User
from app.database.session import get_db
from app.utils import get_current_user, hash_password, verify_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/me", response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile.
    """
    return UserResponse.from_orm(current_user)

@router.put("/me", response_model=StandardResponse)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update info the current user's profile.
    """
    # Update the user's profile
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return StandardResponse(message="Profile updated successfully")

@router.put("/me/email", response_model=StandardResponse)
def update_email(
    email_update: EmailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.email == email_update.new_email:
        raise HTTPException(status_code=400, detail="New email cannot be the same as the current email")
    
    if email_update.new_email != email_update.confirm_new_email:
        raise HTTPException(status_code=400, detail="New email and confirmation do not match")

    check_email = db.query(User).filter(User.email == email_update.new_email).first()
    if check_email:
        raise HTTPException(status_code=400, detail="Email already in use")

    current_user.email = email_update.new_email
    db.commit()
    db.refresh(current_user)

    return StandardResponse(message="Email updated successfully")

@router.put("/me/password", response_model=StandardResponse)
def update_password(
    password_update: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update password the current users's
    """
    if  not verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if password_update.current_password == password_update.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as the current password")

    if password_update.new_password != password_update.confirm_new_password:
        raise HTTPException(status_code=400, detail="New password and confirmation do not match")
    
    current_user.hashed_password = hash_password(password_update.new_password)
    db.commit()
    db.refresh(current_user)

    return StandardResponse(message="Password updated successfully")

@router.delete("/me", response_model=StandardResponse)
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete the current user's profile.
    """
    db.delete(current_user)
    db.commit()

    return StandardResponse(message="Profile deleted successfully")