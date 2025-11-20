from sqlalchemy import Column, String, DECIMAL, DateTime, Text, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, GUID

class Statement(Base):
    __tablename__ = "statements"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    file_upload_id = Column(GUID(), ForeignKey("file_uploads.id"), nullable=True)
    account_id = Column(GUID(), ForeignKey("accounts.id"), nullable=True)

    statement_type = Column(String(50), nullable=True)
    filename = Column(String(255), nullable=True)
    status = Column(String(20), default="processed", nullable=False)
    review_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="statements")
    file_upload = relationship("FileUpload", back_populates="statements")
    account = relationship("Account")
    transactions = relationship("Transaction", back_populates="statement")