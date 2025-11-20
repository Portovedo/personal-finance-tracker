from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.ai_advisor import AIAdvisor

router = APIRouter()
advisor = AIAdvisor()

@router.get("/advice")
async def get_financial_advice(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generates personalized financial advice using Gemini AI.
    """
    return advisor.generate_advice(db, str(current_user.id))