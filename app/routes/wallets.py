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

    Each wallet includes the following fields:
    - **id**: Unique identifier of the wallet.
    - **name**: Name of the wallet.
    - **balance**: Current balance of the wallet.
    - **currency**: Currency of the wallet.
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

    The wallet must include the following fields:
    - **name**: Name of the wallet (required).
    - **balance**: Initial balance of the wallet (optional, default is 0).
    - **currency**: Currency of the wallet (optional, default is "IDR").
    - **description**: Description of the wallet (optional).
    """
    new_wallet = Wallet(**wallet.dict(), user_id=user.id)

    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)

    return StandardResponse(
        message="Wallet created successfully",
        data=WalletResponse.from_orm(new_wallet)
    )
