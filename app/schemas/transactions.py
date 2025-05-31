from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
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
    wallet_currency: str

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

class TransactionSummaryItem(BaseModel):
    period: str
    total_income: float
    total_expense: float
    balance: float
    income_count: int
    expense_count: int

class TransactionSummaryGroupedResponse(BaseModel):
    summary: List[TransactionSummaryItem]

class TransactionSummaryFilter(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    category_id: Optional[UUID] = None
    wallet_id: Optional[UUID] = None
    group_by: Optional[str] = "month"