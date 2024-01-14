from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.types import Gender, Role


class User(BaseModel):
    id: int
    email: str
    phone: str
    role: Role
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
