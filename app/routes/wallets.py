from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.wallets import *
from app.schemas.responses import StandardResponse
from app.database.session import get_db
from app.database.models.users import User
from app.database.models.wallets import Wallet
from app.routes.users import get_current_user

router = APIRouter()


@router.get("/", response_model=list[WalletResponse])
async def get_wallets(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get all wallets of the current user.
    """
    return db.query(Wallet).filter(Wallet.user_id == user.id).all()


@router.post("/", response_model=StandardResponse)
async def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Create a new wallet for the current user.
    """

    check_wallet = db.query(Wallet).filter(
        Wallet.name == wallet.name,
        Wallet.user_id == user.id
    ).first()

    if check_wallet:
        raise HTTPException(status_code=400, detail="Wallet name already exists")
    
    new_wallet = Wallet(**wallet.dict(), user_id=user.id)

    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)

    return StandardResponse(
        message="Wallet created successfully",
        data=WalletResponse.from_orm(new_wallet)
    )


# @router.get("/{wallet_id}", response_model=WalletResponse)
# def get_wallet(wallet_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
#     if not wallet:
#         raise HTTPException(404, detail="Wallet not found")
#     return wallet

# @router.put("/{wallet_id}", response_model=WalletResponse)
# def update_wallet(wallet_id: UUID, data: WalletUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
#     if not wallet:
#         raise HTTPException(404, detail="Wallet not found")
    
#     for key, value in data.dict(exclude_unset=True).items():
#         setattr(wallet, key, value)

#     db.commit()
#     db.refresh(wallet)
#     return wallet

# @router.delete("/{wallet_id}")
# def delete_wallet(wallet_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user.id).first()
#     if not wallet:
#         raise HTTPException(404, detail="Wallet not found")
#     db.delete(wallet)
#     db.commit()
#     return {"message": "Wallet deleted successfully"}

# @router.get("/summary", response_model=WalletSummary)
# def wallet_summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     wallets = db.query(Wallet).filter(Wallet.user_id == user.id).all()
#     total = sum(w.balance for w in wallets)
#     return WalletSummary(total_wallets=len(wallets), total_balance=total)