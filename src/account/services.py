from sqlalchemy.orm import Session

from account.auth import hash_password
from account.enums import UserRole
from account.models import UserModel
from account.schemas import User, UserCreate


def get_user_detail(db: Session, id: int) -> User:
    db_user = db.query(UserModel).filter(UserModel.id == id).one_or_none()
    if not db_user:
        raise ValueError("User not found")
    return User(**db_user.__dict__)


def register_user(db: Session, user: UserCreate) -> User:
    if db.query(UserModel).filter(UserModel.email == user.email).one_or_none():
        raise ValueError("User with this email already exists")

    if db.query(UserModel).filter(UserModel.phone == user.phone).one_or_none():
        raise ValueError("User with this phone already exists")

    db_user = UserModel(
        email=user.email,
        phone=user.phone,
        password=hash_password(plain_password=user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender.value if user.gender else None,
        role=UserRole.MANUFACTURER.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)
