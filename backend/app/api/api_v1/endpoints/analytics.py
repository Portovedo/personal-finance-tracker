from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/net-worth")
async def get_net_worth_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    
    assets = sum(acc.current_balance for acc in accounts if acc.type not in ['credit_card', 'loan', 'mortgage'])
    liabilities = sum(acc.current_balance for acc in accounts if acc.type in ['credit_card', 'loan', 'mortgage'])
    
    portfolio_value = 0
    for portfolio in current_user.portfolios:
        portfolio_value += float(portfolio.total_value or 0)

    return {
        "current_net_worth": float(assets + portfolio_value) - float(liabilities),
        "assets": float(assets + portfolio_value),
        "liabilities": float(liabilities),
        "currency": current_user.currency
    }

@router.get("/spending")
async def get_spending_by_category(
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict]:
    if not month or not year:
        now = datetime.now()
        month = now.month
        year = now.year

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    results = db.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction.category)\
     .filter(
         Transaction.user_id == current_user.id,
         Transaction.transaction_date >= start_date,
         Transaction.transaction_date < end_date,
         Transaction.type == 'debit' 
     ).group_by(Category.id, Category.name, Category.color).all()

    return [
        {
            "category": name,
            "color": color,
            "amount": float(total),
            "currency": current_user.currency
        }
        for name, color, total in results
    ]

@router.get("/income")
async def get_income_vs_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return []