from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from account.enums import Gender, UserRole


class User(BaseModel):
    id: int
    email: EmailStr
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
    email: EmailStr
    password: str
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None


class Authenticate(BaseModel):
    email: EmailStr
    password: str
