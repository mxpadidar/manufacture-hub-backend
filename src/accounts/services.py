from datetime import datetime

from jose import jwt
from sqlalchemy.orm import Session

from accounts import cruds
from accounts.models import User, UserCreate
from core.configs import jwt_configs, pwd_context
from core.types import Role, Token, TokenPayload


def create_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def create_token(payload: TokenPayload) -> Token:
    token = jwt.encode(
        claims={
            "id": payload.id,
            "role": payload.role,
            "exp": datetime.utcnow() + jwt_configs.expires_in,
        },
        key=jwt_configs.secret,
        algorithm=jwt_configs.algorithm,
    )
    return Token(value=token, type="bearer")


def users(db: Session) -> list[User]:
    db_users = cruds.get_users(db=db)
    return [User(**user.__dict__) for user in db_users]


def user_details(db: Session, id: int) -> User:
    db_user = cruds.get_user_by_id(db=db, id=id)
    if not db_user:
        raise ValueError("User not found")
    return User(**db_user.__dict__)


def user_register(db: Session, user: UserCreate) -> User:
    if cruds.get_user_by_email(db, user.email):
        raise ValueError("User with this email already exists")

    if cruds.get_user_by_phone(db, user.phone):
        raise ValueError("User with this phone already exists")

    new_user = cruds.create_user(
        db=db,
        email=user.email,
        hashed_password=create_hashed_password(user.password),
        phone=user.phone,
        role_id=Role.MANUFACTURER.value,
        first_name=user.first_name,
        last_name=user.last_name,
        gender_id=user.gender.value if user.gender else None,
    )
    return User(**new_user.__dict__)
