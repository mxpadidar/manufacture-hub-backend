from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from account.deps import get_current_user
from account.schemas import Tokens, User, UserLogin, UserRegister
from account.services import (
    authenticate,
    generate_user_tokens,
    refresh_access_token,
    register_user,
)
from core.deps import get_db
from core.errors import AuthErr, ConflictErr, InvalidTokenErr, NotFoundErr
from core.exceptions import ConflictExp, NotFoundExp, UnAuthorizedExp

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register")
def user_register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = register_user(data=data, db=db)
        return generate_user_tokens(user_id=user.id, user_role_id=user.role.value)
    except ConflictErr:
        raise ConflictExp


@router.post("/tokens")
def get_tokens(data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate(db=db, email=data.email, password=data.password)
        return generate_user_tokens(user_id=user.id, user_role_id=user.role.value)
    except NotFoundErr:
        raise NotFoundExp
    except AuthErr:
        raise UnAuthorizedExp


@router.post("/tokens/refresh")
def refresh_token(data: Tokens, db: Session = Depends(get_db)):
    try:
        access_token = refresh_access_token(tokens=data, db=db)
        return {"access_token": access_token}
    except InvalidTokenErr:
        raise UnAuthorizedExp


@router.get("/profile")
def user_profile(user: User = Depends(get_current_user)):
    return user
