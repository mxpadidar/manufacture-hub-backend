from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]
    exp: Optional[datetime]


class Login(BaseModel):
    email: EmailStr
    password: str
