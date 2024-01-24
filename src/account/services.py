from datetime import datetime

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from account.enums import UserRole
from account.models import UserModel
from account.schemas import Token, TokenData, User, UserCreate
from core.errors import AuthErr, ConflictErr, NotFoundErr
from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role_id: int) -> Token:
    expires_date = datetime.utcnow() + settings.jwt_expires_in
    token = jwt.encode(
        claims={"user_id": user_id, "role_id": role_id, "exp": expires_date},
        key=settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return Token(access_token=token, token_type="bearer")


def get_token_data(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = payload.get("user_id")
        role_id = payload.get("role_id")
        exp = payload.get("exp")
        if not (user_id and role_id and exp):
            return None
        return TokenData(
            user_id=payload.get("user_id"),
            role_id=payload.get("role_id"),
            exp=payload.get("exp"),
        )
    except JWTError:
        return None
