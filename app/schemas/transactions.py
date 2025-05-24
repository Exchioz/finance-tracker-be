from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID

from .enums import TransactionType

class TransactionDetailResponse(BaseModel):
    id: UUID
    name: str
    amount: Decimal
    type: TransactionType
    description: str
    date: datetime
    category_name: str
    wallet_name: str

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: UUID
    name: str
    amount: Decimal
    type: TransactionType
    date: datetime
    category_name: str
    wallet_name: str

    class Config:
        from_attributes = True

class PaginatedTransactionResponse(BaseModel):
    data: list[TransactionResponse]
    page: int
    limit: int
    total: int

class TransactionCreate(BaseModel):
    name: str
    amount: Decimal
    type: TransactionType
    description: str = ""
    date: datetime = datetime.now(timezone.utc)
    category_id: UUID
    wallet_id: UUID

class TransactionUpdate(BaseModel):
    name: str | None = None
    amount: Decimal | None = None
    type: TransactionType | None = None
    description: str | None = None
    date: datetime | None = None
    category_id: UUID | None = None
    wallet_id: UUID | None = None