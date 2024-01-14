from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from core.configs import Base


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "account"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[Optional[int]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    last_login: Mapped[Optional[datetime]]
    deleted_at: Mapped[Optional[datetime]]
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
