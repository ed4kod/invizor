from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User схемы
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Account схемы
class AccountBase(BaseModel):
    name: str
    description: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Asset схемы
class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"
    image_filename: Optional[str] = None

class AssetCreate(AssetBase):
    account_id: int

class Asset(AssetBase):
    id: int
    account_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token схема
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 