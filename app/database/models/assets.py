import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Numeric, ForeignKey, Enum, Text, DateTime
from datetime import datetime, timezone

from app.database.base import Base

class AssetType(str, enum.Enum):
    cash = "cash"
    investment  = "investment"
    property = "property"
    other = "other"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False)
    
    name = Column(String(100), nullable=False)
    type = Column(Enum(AssetType), nullable=False)
    unit = Column(Numeric(20, 8), nullable=False)
    unit_price = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(3), default="IDR")
    time = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="assets")
    wallet = relationship("Wallet", back_populates="assets")

    @property
    def total_value(self):
        return self.unit * self.unit_price