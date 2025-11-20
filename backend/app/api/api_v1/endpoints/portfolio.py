
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio, PortfolioHolding
from app.schemas.portfolio import PortfolioCreate, PortfolioHoldingCreate, PortfolioResponse
from app.services.auth_service import get_current_user
from app.services.market_data_service import MarketDataService
from app.services.plaid_service import PlaidService

router = APIRouter()

@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new portfolio.
    """
    db_portfolio = Portfolio(**portfolio.dict(), user_id=current_user.id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific portfolio.
    """
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/{portfolio_id}/holdings", response_model=PortfolioResponse)
async def add_holding_to_portfolio(
    portfolio_id: str,
    holding: PortfolioHoldingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a holding to a portfolio.
    """
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db_holding = PortfolioHolding(**holding.dict(), portfolio_id=portfolio.id, user_id=current_user.id)
    db.add(db_holding)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.post("/update-prices")
async def update_prices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the current prices of all portfolio holdings for the current user.
    """
    market_data_service = MarketDataService(db)
    market_data_service.update_portfolio_holdings_prices(current_user.id)
    return {"message": "Prices updated successfully"}

@router.post("/plaid/create-link-token")
async def create_link_token(current_user: User = Depends(get_current_user)):
    """
    Create a Plaid link token.
    """
    plaid_service = PlaidService()
    return plaid_service.create_link_token(str(current_user.id))

@router.post("/plaid/exchange-public-token")
async def exchange_public_token(public_token: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Exchange a Plaid public token for an access token.
    """
    plaid_service = PlaidService()
    response = plaid_service.exchange_public_token(public_token)

    # Save the access token to the user's portfolio
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if portfolio:
        portfolio.plaid_access_token = response['access_token']
        portfolio.plaid_item_id = response['item_id']
        db.commit()

    return response

@router.post("/plaid/sync-investments")
async def sync_investments(access_token: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Sync investment holdings from Plaid.
    """
    plaid_service = PlaidService()
    response = plaid_service.get_investment_holdings(access_token)

    # Process and save the holdings to the database
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id, Portfolio.plaid_access_token == access_token).first()
    if portfolio:
        for holding in response['holdings']:
            db_holding = db.query(PortfolioHolding).filter(PortfolioHolding.portfolio_id == portfolio.id, PortfolioHolding.symbol == holding['security']['symbol']).first()
            if db_holding:
                db_holding.quantity = holding['quantity']
                db_holding.avg_cost = holding['cost_basis']
                db_holding.current_price = holding['security']['close_price']
                db_holding.current_value = holding['quantity'] * holding['security']['close_price']
            else:
                db_holding = PortfolioHolding(
                    portfolio_id=portfolio.id,
                    user_id=current_user.id,
                    symbol=holding['security']['symbol'],
                    security_name=holding['security']['name'],
                    quantity=holding['quantity'],
                    avg_cost=holding['cost_basis'],
                    current_price=holding['security']['close_price'],
                    current_value=holding['quantity'] * holding['security']['close_price'],
                    asset_type='stock', # This is a placeholder
                )
                db.add(db_holding)
        db.commit()

    return response
