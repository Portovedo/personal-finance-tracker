
import yfinance as yf
from sqlalchemy.orm import Session
from app.models.portfolio import PortfolioHolding

class MarketDataService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_price(self, symbol: str) -> float | None:
        """
        Gets the current price of a stock.
        """
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")
        if not history.empty:
            return history['Close'].iloc[-1]
        return None

    def update_portfolio_holdings_prices(self, user_id: str):
        """
        Updates the current price of all portfolio holdings for a user.
        """
        holdings = self.db.query(PortfolioHolding).filter(PortfolioHolding.user_id == user_id).all()
        for holding in holdings:
            current_price = self.get_current_price(holding.symbol)
            if current_price:
                holding.current_price = current_price
                holding.current_value = holding.quantity * current_price
        self.db.commit()
