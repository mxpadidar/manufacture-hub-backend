from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from account.services import authenticate
from auth.schemas import Login
from auth.services import create_access_token
from core.dependencies import get_db
from core.errors import AuthErr, NotFoundErr
from core.exceptions import NotFoundExp, UnAuthorizedExp

router = APIRouter(prefix="/auth", tags=["auth"])


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
