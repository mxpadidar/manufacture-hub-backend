from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from accounts.cruds import find_by_email, register_user
from accounts.models import UserCreate
from core.dependencies import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{email}")
def user_detail(email: str, db: Session = Depends(get_db)):
    user = find_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(user=user, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
