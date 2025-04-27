from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class WalletResponse(BaseModel):
    id: UUID
    name: str
    balance: Decimal
    currency: str
    description: str | None = None

    class Config:
        from_attributes = True

class WalletCreate(BaseModel):
    name: str
    balance: Decimal= 0
    currency: str = "IDR"
    description: str | None = None

class WalletUpdate(BaseModel):
    name: str | None = None
    balance: Decimal | None = None
    currency: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True

class WalletSummary(BaseModel):
    total_wallets: int
    total_balance: Decimal
    
    class Config:
        from_attributes = True