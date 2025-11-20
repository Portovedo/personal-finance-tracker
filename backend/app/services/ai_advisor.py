import google.generativeai as genai
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIAdvisor:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        else:
            self.model = None

    def generate_advice(self, db: Session, user_id: str):
        if not self.model:
            return {
                "error": "Gemini API Key is missing. Please add GEMINI_API_KEY to your .env file."
            }

        # 1. Gather Context Data
        accounts = db.query(Account).filter(Account.user_id == user_id).all()
        net_worth = sum(a.current_balance for a in accounts)
        
        # Get last month's spending by category
        spending = db.query(
            Category.name, func.sum(Transaction.amount)
        ).join(Transaction.category).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'debit'
        ).group_by(Category.name).limit(5).all()

        spending_summary = ", ".join([f"{cat}: ${val:.2f}" for cat, val in spending])

        # 2. Construct Prompt
        prompt = f"""
        You are an expert personal finance advisor. Here is my current financial snapshot:
        - Total Net Worth: ${net_worth:.2f}
        - Top Spending Categories (Last Month): {spending_summary}
        
        Please provide:
        1. A brief analysis of my financial health.
        2. Three specific, actionable tips to save more money based on my spending.
        3. A general trick or strategy for better investing or wealth management suitable for this profile.
        
        Format the output as HTML (use <h3> for headers, <ul>/<li> for lists, <p> for text). Do not include ```html blocks.
        """

        try:
            response = self.model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            logger.error(f"AI Generation failed: {e}")
            return {"error": "Failed to generate advice. Please try again later."}