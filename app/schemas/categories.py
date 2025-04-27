from pydantic import BaseModel
from uuid import UUID

from app.database.models.enums import CategoriesType

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    type: CategoriesType
    description: str | None = None

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    type: CategoriesType
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoriesType | None = None
    description: str | None = None