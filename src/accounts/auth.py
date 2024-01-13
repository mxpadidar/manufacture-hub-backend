from datetime import datetime

from jose import jwt

from core.configs import jwt_configs, pwd_context
from core.types import Token, TokenPayload


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
