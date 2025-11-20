
from pydantic import BaseModel
import uuid
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: str
    transaction_date: datetime

class TransactionResponse(TransactionBase):
    id: uuid.UUID
    account_id: uuid.UUID
    category_id: uuid.UUID | None = None

    class Config:
        orm_mode = True
