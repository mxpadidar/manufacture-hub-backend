from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[Optional[int]] = mapped_column(Integer)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())

    tokens = relationship("TokenModel", back_populates="user")


class TokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user = relationship("UserModel", back_populates="tokens")
