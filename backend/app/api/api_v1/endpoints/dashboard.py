
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a summary of the user's financial data for the dashboard.
    """
    # Calculate net worth
    total_account_balance = sum(account.current_balance for account in current_user.accounts)
    total_portfolio_value = sum(holding.current_value for portfolio in current_user.portfolios for holding in portfolio.holdings)
    net_worth = total_account_balance + total_portfolio_value

    # Calculate asset allocation
    asset_allocation = {}
    for portfolio in current_user.portfolios:
        for holding in portfolio.holdings:
            asset_type = holding.asset_type
            if asset_type not in asset_allocation:
                asset_allocation[asset_type] = 0
            asset_allocation[asset_type] += holding.current_value

    # TODO: Calculate portfolio value over time
    portfolio_value_over_time = []

    summary_data = {
        "net_worth": net_worth,
        "asset_allocation": asset_allocation,
        "portfolio_value_over_time": portfolio_value_over_time,
    }
    return summary_data
