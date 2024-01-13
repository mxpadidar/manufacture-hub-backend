from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.configs import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[Optional[int]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    last_login: Mapped[Optional[datetime]]
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
    deleted_at: Mapped[Optional[datetime]]
