from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal

class WalletResponse(BaseModel):
    id: UUID
    name: str
    balance: Decimal
    currency: str
    description: Optional[str]

    class Config:
        from_attributes = True

class WalletCreate(BaseModel):
    name: str
    balance: Optional[Decimal] = 0
    currency: Optional[str] = "IDR"
    description: Optional[str] = None

class WalletUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[Decimal] = None
    currency: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class WalletSummary(BaseModel):
    total_wallets: int
    total_balance: Decimal
    
    class Config:
        from_attributes = True