from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class CurrencyBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=3)
    name: str

class CurrencyOut(CurrencyBase):
    id: int

    class Config:
        from_attributes = True

class UserWithSubscriptions(UserOut):
    subscriptions: List[CurrencyOut] = []

class SubscriptionCreate(BaseModel):
    user_id: int
    currency_code: str

# Это нужно, чтобы ForwardRef разрешился правильно
UserWithSubscriptions.model_rebuild()
