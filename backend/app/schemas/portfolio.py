
from pydantic import BaseModel
import uuid
from typing import List

class PortfolioHoldingBase(BaseModel):
    symbol: str
    quantity: float
    avg_cost: float

class PortfolioHoldingCreate(PortfolioHoldingBase):
    pass

class PortfolioHoldingResponse(PortfolioHoldingBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioResponse(PortfolioBase):
    id: uuid.UUID
    user_id: uuid.UUID
    holdings: List[PortfolioHoldingResponse] = []

    class Config:
        orm_mode = True
