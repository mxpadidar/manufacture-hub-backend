from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import Mapped, mapped_column

from account.enums import Gender, UserRole
from core.db import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(String(50), default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)

    def __init__(
        self,
        email: str,
        phone: str,
        password: str,
        role: UserRole,
        gender: Gender,
        first_name: str,
        last_name: str,
    ):
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.last_login = datetime.utcnow()
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update(
        self,
        phone: Optional[str] = None,
        gender: Optional[Gender] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        last_login: Optional[datetime] = None,
    ):
        self.phone = phone or self.phone
        self.gender = gender or self.gender
        self.first_name = first_name or self.first_name
        self.last_name = last_name or self.last_name
        self.is_active = is_active or self.is_active
        self.last_login = last_login or self.last_login
        self.updated_at = datetime.utcnow()

    def login(self):
        self.last_login = datetime.utcnow()


class RevokedTokenDB(Base):
    __tablename__ = "revoked_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id
        self.revoked_at = datetime.utcnow()
