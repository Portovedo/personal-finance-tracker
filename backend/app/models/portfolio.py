from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, GUID

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    total_value = Column(String(19), default="0")

    user = relationship("User", back_populates="portfolios")
    holdings = relationship("PortfolioHolding", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("PortfolioTransaction", back_populates="portfolio", cascade="all, delete-orphan")

class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(GUID(), ForeignKey("portfolios.id"), nullable=False)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)

    symbol = Column(String(20), nullable=False)
    quantity = Column(String(19), nullable=False)
    avg_cost = Column(String(19), nullable=False)
    current_value = Column(String(19), default="0")

    portfolio = relationship("Portfolio", back_populates="holdings")
    transactions = relationship("PortfolioTransaction", back_populates="holding")

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(GUID(), ForeignKey("portfolios.id"), nullable=False)
    holding_id = Column(GUID(), ForeignKey("portfolio_holdings.id"), nullable=True)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    
    symbol = Column(String(20), nullable=False)
    quantity = Column(String(19), nullable=False)
    
    portfolio = relationship("Portfolio", back_populates="transactions")
    holding = relationship("PortfolioHolding", back_populates="transactions")