from datetime import datetime

from pydantic import BaseModel, EmailStr

from account.enums import Gender, UserRole


class User(BaseModel):
    id: int
    email: EmailStr
    phone: str
    role: UserRole
    gender: Gender
    first_name: str
    last_name: str
    created_at: datetime
    last_login: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    phone: str
    first_name: str
    last_name: str
    gender: Gender


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: int
    role_id: int
    expires_at: datetime
