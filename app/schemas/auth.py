from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., min_length=8, max_length=128, example="password123")
    full_name: str = Field(..., min_length=1, max_length=100, example="John Doe")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="email@example.com")
    password: str = Field(..., min_length=1, max_length=128, example="password123")

class LoginData(BaseModel):
    access_token: str
    token_type: str = 'bearer'