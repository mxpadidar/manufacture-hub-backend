from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from account.enums import Gender, UserRole


class User(BaseModel):
    id: int
    email: str
    phone: str
    role: UserRole
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[Gender]
    last_login: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class UserCreate(BaseModel):
    email: str
    password: str
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None


class Token(BaseModel):
    value: str
    type: str
