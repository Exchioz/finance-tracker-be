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

    model_config = {
        "from_attributes": True
    }

class WalletCreate(BaseModel):
    name: str
    balance: Optional[Decimal] = 0
    currency: Optional[str] = "IDR"
    description: Optional[str] = None