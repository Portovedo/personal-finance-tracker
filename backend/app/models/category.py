from sqlalchemy import Column, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, GUID

class Category(Base):
    __tablename__ = "categories"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    parent_category_id = Column(GUID(), ForeignKey("categories.id"), nullable=True)

    name = Column(String(255), nullable=False)
    color = Column(String(7), default="#6B7280", nullable=False)
    type = Column(String(20), nullable=False) # income, expense
    is_system = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    rules = relationship("CategoryRule", back_populates="category", cascade="all, delete-orphan")

class CategoryRule(Base):
    __tablename__ = "category_rules"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    category_id = Column(GUID(), ForeignKey("categories.id"), nullable=False)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)

    rule_type = Column(String(20), nullable=False)
    rule_value = Column(String(500), nullable=False)
    
    category = relationship("Category", back_populates="rules")