import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Numeric, ForeignKey

from app.database.base import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(100), unique=True, nullable=False)
    balance = Column(Numeric(12, 2), default=0)
    currency = Column(String(3), default="IDR")
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="wallets")
    assets = relationship("Asset", back_populates="wallet", cascade="all, delete")