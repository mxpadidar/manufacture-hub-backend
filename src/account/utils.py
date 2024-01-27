from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from account.schemas import TokenData
from core.errors import InvalidTokenErr
from core.settings import JWT_ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_jwt(data: TokenData) -> str:
    return jwt.encode(
        claims={
            "user_id": data.user_id,
            "role_id": data.role_id,
            "expires_at": data.expires_at.isoformat(),
        },
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_jwt(token: str) -> TokenData:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return TokenData.model_validate(payload)
    except JWTError:
        raise InvalidTokenErr("Invalid JWT: Unable to decode")
    except ValidationError:
        raise InvalidTokenErr("Invalid JWT: Payload does not match required format")
