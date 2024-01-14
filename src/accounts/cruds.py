from sqlalchemy.orm import Session

from accounts.auth import create_hashed_password, create_token
from accounts.database import UserModel
from accounts.models import User, UserCreate
from core.types import Role, Token, TokenPayload


def find_by_email(db: Session, email: str) -> User | None:
    db_user = db.query(UserModel).filter(UserModel.email == email).one_or_none()
    return User(**db_user.__dict__) if db_user else None


def find_by_phone(db: Session, phone: str) -> User | None:
    db_user = db.query(UserModel).filter(UserModel.phone == phone).one_or_none()
    return User(**db_user.__dict__) if db_user else None


def create_user(db: Session, user: UserCreate, role: Role) -> User:
    if find_by_email(db, user.email):
        raise ValueError("User with this email already exists")

    if find_by_phone(db, user.phone):
        raise ValueError("User with this phone already exists")

    db_user = UserModel(
        email=user.email,
        password=create_hashed_password(user.password),
        phone=user.phone,
        role=role.value,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender.value if user.gender else None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


def register_user(db: Session, user: UserCreate) -> Token:
    new_user = create_user(db=db, user=user, role=Role.MANUFACTURER)
    return create_token(TokenPayload(id=new_user.id, role=new_user.role.value))
