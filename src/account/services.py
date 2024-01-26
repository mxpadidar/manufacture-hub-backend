from datetime import datetime

from sqlalchemy.orm import Session

from account.db_models import RevokedTokenDB, UserDB
from account.enums import UserRole
from account.schemas import TokenData, Tokens, User, UserRegister
from account.utils import decode_jwt, generate_jwt, hash_password, verify_password
from core.errors import AuthErr, ConflictErr, NotFoundErr
from core.settings import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME


def get_user(db: Session, id: int) -> User:
    db_user = db.query(UserDB).filter(UserDB.id == id).one_or_none()
    if not db_user:
        raise NotFoundErr("User not found")
    return User(**db_user.__dict__)


def register_user(data: UserRegister, db: Session) -> User:
    if db.query(UserDB).filter(UserDB.email == data.email).one_or_none():
        raise ConflictErr("User with this email already exists")

    if db.query(UserDB).filter(UserDB.phone == data.phone).one_or_none():
        raise ConflictErr("User with this phone already exists")

    user_db = UserDB(
        **data.model_dump(exclude={"password"}),
        password=hash_password(data.password),
        role=UserRole.OWNER,
    )
    db.add(user_db)
    db.commit()

    return User(**user_db.__dict__)


def authenticate(db: Session, email: str, password: str) -> User:
    db_user = db.query(UserDB).filter(UserDB.email == email).one_or_none()
    if not db_user:
        raise NotFoundErr("User not found")

    if not verify_password(plain_password=password, hashed_password=db_user.password):
        raise AuthErr("Incorrect password")

    db_user.update(last_login=datetime.utcnow())
    db.commit()
    db.refresh(db_user)

    return User(**db_user.__dict__)


def generate_user_tokens(user_id: int, user_role_id: int) -> dict:
    access_token = generate_jwt(
        data=TokenData(
            expires_at=datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
            user_id=user_id,
            role_id=user_role_id,
        )
    )
    refresh_token = generate_jwt(
        data=TokenData(
            expires_at=datetime.utcnow() + REFRESH_TOKEN_LIFETIME,
            user_id=user_id,
            role_id=user_role_id,
        )
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_access_token(tokens: Tokens, db: Session) -> str:
    refresh_token_data = decode_jwt(token=tokens.refresh_token)

    new_access_token = generate_jwt(
        data=TokenData(
            expires_at=datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
            user_id=refresh_token_data.user_id,
            role_id=refresh_token_data.role_id,
        )
    )

    db.add(
        RevokedTokenDB(
            token=tokens.access_token,
            user_id=refresh_token_data.user_id,
        )
    )

    db.commit()
    return new_access_token
