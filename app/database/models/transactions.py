import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, ForeignKey
from datetime import datetime, timezone

from app.schemas.enums import TransactionType
from app.database.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String, default="")
    date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")