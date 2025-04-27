from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.categories import *
from app.schemas.responses import StandardResponse
from app.database.session import get_db
from app.database.models import User, Category
from app.routes.users import get_current_user

router = APIRouter()

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    category = db.query(Category)\
        .filter(Category.user_id == user.id)
    
    return category

@router.post("/", response_model=StandardResponse)
async def create_categories(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if db.query(Category).filter(Category.name == category.name, Category.user_id == user.id).first():
        raise HTTPException(400, "Wallet name already exists")
    
    new_categories = Category(**category.dict(), user_id=user.id)
    db.add(new_categories)

    db.flush()
    db.refresh(new_categories)

    return StandardResponse(
        message="Category created successfully"
    )

@router.put("/{category_id}", response_model=StandardResponse)
async def update_category(
    category_id: UUID,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    
    if not db_category:
        raise HTTPException(404, "Category not found")
    
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()

    return StandardResponse(
        message="Category updated successfully",
        data=CategoryResponse.from_orm(db_category)
    )

@router.delete("/{category_id}", response_model=StandardResponse)
async def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    
    if not db_category:
        raise HTTPException(404, "Category not found")
    
    db.delete(db_category)
    db.commit()

    return StandardResponse(message="Category deleted successfully")