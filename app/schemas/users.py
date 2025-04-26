from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserUpdate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100, example="John Doe")

class EmailUpdate(BaseModel):
    new_email: EmailStr = Field(..., example="email@example.com")
    confirm_new_email: EmailStr = Field(..., example="email@example.com")

class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128, example="current_password123")
    new_password: str = Field(..., min_length=8, max_length=128, example="new_password123")
    confirm_new_password: str = Field(..., min_length=8, max_length=128, example="new_password123")

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True