
from pydantic import BaseModel
import uuid

class AccountBase(BaseModel):
    name: str
    type: str
    current_balance: float

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True
