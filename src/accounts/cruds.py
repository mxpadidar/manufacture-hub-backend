from typing import Optional

from sqlalchemy.orm import Session

from accounts.database import UserModel


def get_users(db: Session) -> list[UserModel]:
    return db.query(UserModel).all()


def get_user_by_id(db: Session, id: int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == id).one_or_none()


def get_user_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).one_or_none()


def get_user_by_phone(db: Session, phone: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.phone == phone).one_or_none()


def create_user(
    db: Session,
    email: str,
    hashed_password: str,
    phone: str,
    role_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender_id: Optional[int] = None,
) -> UserModel:
    db_user = UserModel(
        email=email,
        password=hashed_password,
        phone=phone,
        role=role_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
