from pydantic import BaseModel
from uuid import UUID

from .enums import TransactionType

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    type: TransactionType
    description: str | None = None

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    type: TransactionType
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = None
    type: TransactionType | None = None
    description: str | None = None