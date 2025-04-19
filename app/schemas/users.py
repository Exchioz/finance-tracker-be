from pydantic import BaseModel, EmailStr, Field, validator
from typing import Any, Optional
from datetime import datetime
from uuid import UUID

class StandardResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., min_length=8, max_length=128, example="password123")
    full_name: str = Field(..., min_length=1, max_length=100, example="John Doe")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., min_length=1, max_length=128, example="password123")

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class LoginData(BaseModel):
    access_token: str
    token_type: str = 'bearer'