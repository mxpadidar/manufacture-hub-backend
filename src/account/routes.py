from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from account.dependencies import get_current_user
from account.schemas import User, UserCreate
from account.services import register_user
from auth.services import create_access_token
from core.dependencies import get_db
from core.errors import ConflictErr
from core.exceptions import ConflictExp

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
