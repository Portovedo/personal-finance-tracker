from sqlalchemy import Column, String, DECIMAL, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, GUID

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    account_id = Column(GUID(), ForeignKey("accounts.id"), nullable=False)
    category_id = Column(GUID(), ForeignKey("categories.id"), nullable=True)

    # Changed Decimal to DECIMAL
    amount = Column(DECIMAL(19, 4), nullable=False)
    description = Column(String(1000), nullable=False)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    
    type = Column(String(20), nullable=False) # debit, credit
    status = Column(String(20), default='completed', nullable=False)
    
    # Transfers
    destination_account_id = Column(GUID(), ForeignKey("accounts.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    destination_account = relationship("Account", back_populates="sent_transfers", foreign_keys=[destination_account_id])
    category = relationship("Category", back_populates="transactions")
    statement = relationship("Statement", back_populates="transactions")
    
    statement_id = Column(GUID(), ForeignKey("statements.id"), nullable=True)