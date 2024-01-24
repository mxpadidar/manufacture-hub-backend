from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from account.models import UserModel
from account.schemas import User
from account.services import get_token_data
from core.dependencies import get_db
from core.exceptions import BadRequestExp, UnAuthorizedExp


def get_token_header(request: Request) -> str:
    authorization: Optional[str] = request.headers.get("Authorization")
    if authorization:
        token = authorization.split(" ")[1]
        return token
    else:
        raise UnAuthorizedExp


def get_current_user(token: str = Depends(get_token_header), db: Session = Depends(get_db)) -> User:
    if (token_data := get_token_data(token=token)) is None:
        raise UnAuthorizedExp

    db_user = db.query(UserModel).filter(UserModel.id == token_data.user_id).one_or_none()
    if not db_user:
        raise BadRequestExp

    return User(**db_user.__dict__)
