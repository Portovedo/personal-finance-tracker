
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=AccountResponse)
async def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new account.
    """
    db_account = Account(**account.dict(), user_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=list[AccountResponse])
async def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all accounts for the current user.
    """
    return db.query(Account).filter(Account.user_id == current_user.id).all()
