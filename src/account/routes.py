from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from account.dependencies import get_current_user
from account.schemas import Login, User, UserCreate
from account.services import authenticate, create_access_token, register_user
from core.dependencies import get_db
from core.errors import AuthErr, ConflictErr, NotFoundErr
from core.exceptions import ConflictExp, NotFoundExp, UnAuthorizedExp

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(user=user, db=db)
        token = create_access_token(user_id=new_user.id, role_id=new_user.role.value)
        return {"user": new_user, "access_token": token}
    except ConflictErr:
        raise ConflictExp


@router.get("/profile")
def user_profile(user: User = Depends(get_current_user)):
    return user


@router.post("/token")
def get_access_token(login_data: Login, db: Session = Depends(get_db)):
    try:
        user = authenticate(db=db, email=login_data.email, password=login_data.password)
        token = create_access_token(user_id=user.id, role_id=user.role.value)
        return token
    except NotFoundErr:
        raise NotFoundExp
    except AuthErr:
        raise UnAuthorizedExp


@router.post("/token/refresh")
def refresh_access_token(refresh: str, db: Session = Depends(get_db)):
    ...
