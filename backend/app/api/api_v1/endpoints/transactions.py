
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/{account_id}", response_model=list[TransactionResponse])
async def get_transactions(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all transactions for a specific account.
    """
    return db.query(Transaction).filter(Transaction.account_id == account_id, Transaction.user_id == current_user.id).all()
