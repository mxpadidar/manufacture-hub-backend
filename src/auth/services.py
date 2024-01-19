from datetime import datetime

from jose import JWTError, jwt
from passlib.context import CryptContext

from auth.schemas import Token, TokenData
from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
