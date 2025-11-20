from sqlalchemy import Column, String, DECIMAL, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, GUID

class Account(Base):
    __tablename__ = "accounts"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False) # checking, savings, etc.
    status = Column(String(20), default='active', nullable=False)

    # Changed Decimal to DECIMAL
    current_balance = Column(DECIMAL(19, 4), default=0, nullable=False)
    institution_name = Column(String(255), nullable=True)
    account_number_last4 = Column(String(4), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    
    # For transfers
    sent_transfers = relationship("Transaction", foreign_keys="Transaction.destination_account_id", back_populates="destination_account")