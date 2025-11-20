
from pydantic import BaseModel
import uuid

class CategoryBase(BaseModel):
    name: str
    type: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True
