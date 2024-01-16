from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from account.schemas import Token
from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    return Token(value=token, type="bearer")
