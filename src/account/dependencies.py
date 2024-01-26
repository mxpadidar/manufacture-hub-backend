from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from account.db_models import UserDB
from account.schemas import User
from account.utils import decode_jwt
from core.dependencies import get_db
from core.exceptions import BadRequestExp, UnAuthorizedExp


def extract_token_from_header(request: Request) -> str:
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization:
        token = authorization.split(" ")[1]
        return token
    else:
        raise UnAuthorizedExp


def get_current_user(
    token: str = Depends(extract_token_from_header), db: Session = Depends(get_db)
) -> User:
    if (token_data := decode_jwt(token=token)) is None:
        raise UnAuthorizedExp

    db_user = db.query(UserDB).filter(UserDB.id == token_data.user_id).one_or_none()
    if not db_user:
        raise BadRequestExp

    return User(**db_user.__dict__)
