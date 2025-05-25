from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, aliased

from app.schemas.transactions import *
from app.schemas.responses import StandardResponse
from app.database.session import get_db
from app.database.models import User, Transaction, Category, Wallet
from app.routes.users import get_current_user

router = APIRouter()

@router.get("/", response_model=PaginatedTransactionResponse)
def get_transactions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=10)
):
    offset = (page - 1) * limit
    total = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .count()
    )

    Cat = aliased(Category)
    Wal = aliased(Wallet)

    transactions = (
        db.query(
            Transaction.id,
            Transaction.name,
            Transaction.amount,
            Transaction.type,
            # Transaction.description,
            Transaction.date,
            Cat.name.label("category_name"),
            Wal.name.label("wallet_name"),
            Wal.currency.label("wallet_currency"),
        )
        .join(Cat, Transaction.category_id == Cat.id)
        .join(Wal, Transaction.wallet_id == Wal.id)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return PaginatedTransactionResponse(
        data=transactions,
        page=page,
        limit=limit,
        total=total
    )

@router.post("/", response_model=StandardResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == data.category_id, Category.user_id == user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or not owned by user")
    wallet = db.query(Wallet).filter(Wallet.id == data.wallet_id, Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found or not owned by user")

    new_transaction = Transaction(**data.dict(), user_id=user.id)
    db.add(new_transaction)

    db.commit()
    db.refresh(new_transaction)

    return StandardResponse(
        message="Transactions created successfully"
    )

@router.get("/{transaction_id}", response_model=StandardResponse)
def get_transaction(
    transaction_id: UUID, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction)\
                    .filter(Transaction.id == transaction_id, Transaction.user_id == user.id)\
                    .first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return StandardResponse(
        message="Transaction fetched successfully",
        data=TransactionResponse.from_orm(transaction)
    )

@router.put("/{transaction_id}", response_model=StandardResponse)
def update_transaction(transaction_id: UUID, data: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    
    db.commit()
    db.refresh(transaction)

    return StandardResponse(
        message="Category updated successfully",
        data=TransactionResponse.from_orm(transaction)
    )

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    
    return StandardResponse(message="Transaction deleted successfully")