from datetime import datetime
from typing import NamedTuple, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")


class Token(NamedTuple):
    access_token: str
    token_type: str


class TokenData(NamedTuple):
    user_id: Optional[int]
    role_id: Optional[int]
    exp: Optional[datetime]


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
    return Token(token, "bearer")


def get_token_data(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenData(
            user_id=payload.get("user_id"),
            role_id=payload.get("role_id"),
            exp=payload.get("exp"),
        )
    except JWTError:
        return None
