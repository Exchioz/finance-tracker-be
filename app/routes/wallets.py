from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.wallets import *
from app.schemas.responses import StandardResponse
from app.database.session import get_db
from app.database.models import User, Wallet
from app.routes.users import get_current_user

router = APIRouter()


@router.get("/", response_model=list[WalletResponse])
async def get_wallets(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """
    Get all wallets of the current user.
    """
    wallet = db.query(Wallet)\
        .filter(Wallet.user_id == user.id)\
        .offset(offset)\
        .limit(limit)\
        .all()

    return wallet

@router.post("/", response_model=StandardResponse)
async def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Create a new wallet for the current user.
    """
    if db.query(Wallet).filter(Wallet.name == wallet.name, Wallet.user_id == user.id).first():
        raise HTTPException(400, "Wallet name already exists")
    
    new_wallet = Wallet(**wallet.dict(), user_id=user.id)
    db.add(new_wallet)

    db.flush()
    db.refresh(new_wallet)
    
    return StandardResponse(
        message="Wallet created successfully",
        data=WalletResponse.from_orm(new_wallet)
    )


@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(
    wallet_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get a specific wallet by ID for the current user.
    """
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(404, detail="Wallet not found")
    
    return WalletResponse.from_orm(wallet)

@router.put("/{wallet_id}", response_model=WalletResponse)
def update_wallet(
    wallet_id: UUID,
    data: WalletUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Update a specific wallet by ID for the current user.
    """
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(404, detail="Wallet not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(wallet, key, value)

    db.flush()
    db.refresh(wallet)

    return WalletResponse.from_orm(wallet)

@router.delete("/{wallet_id}", response_model=StandardResponse)
def delete_wallet(
    wallet_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
    if not wallet:
        raise HTTPException(404, detail="Wallet not found")
    
    db.delete(wallet)

    return StandardResponse(message="Wallet deleted successfully")