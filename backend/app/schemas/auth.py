from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import re
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8: # Keeping it simple for local app
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    user_id: Optional[str] = None