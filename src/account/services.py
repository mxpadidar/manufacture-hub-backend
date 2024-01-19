from sqlalchemy.orm import Session

from account.enums import UserRole
from account.models import UserModel
from account.schemas import User, UserCreate
from auth.services import hash_password, verify_password
from core.errors import AuthErr, ConflictErr, NotFoundErr


def get_user(db: Session, id: int) -> User:
    db_user = db.query(UserModel).filter(UserModel.id == id).one_or_none()
    if not db_user:
        raise NotFoundErr("User not found")
    return User(**db_user.__dict__)


def register_user(db: Session, user: UserCreate) -> User:
    if db.query(UserModel).filter(UserModel.email == user.email).one_or_none():
        raise ConflictErr("User with this email already exists")

    if db.query(UserModel).filter(UserModel.phone == user.phone).one_or_none():
        raise ConflictErr("User with this phone already exists")

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


def authenticate(db: Session, email: str, password: str) -> User:
    db_user = db.query(UserModel).filter(UserModel.email == email).one_or_none()
    if not db_user:
        raise NotFoundErr("User not found")

    if not verify_password(plain_password=password, hashed_password=db_user.password):
        raise AuthErr("Incorrect password")

    return User(**db_user.__dict__)
