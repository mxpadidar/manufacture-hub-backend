from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from account import services
from account.auth import create_access_token
from account.schemas import UserCreate
from core.dependencies import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = services.register_user(user=user, db=db)
        token = create_access_token(user_id=new_user.id, role_id=new_user.role.value)
        return {"user": new_user, "access_token": token}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{id}")
def user_detail(id: int, db: Session = Depends(get_db)):
    try:
        return services.get_user_detail(db=db, id=id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
