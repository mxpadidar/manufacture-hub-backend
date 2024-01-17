from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from account import services
from account.schemas import Authenticate, UserCreate
from core.dependencies import get_db
from core.security import create_access_token

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = services.register_user(user=user, db=db)
        token = create_access_token(user_id=new_user.id, role_id=new_user.role.value)
        return {"user": new_user, "access_token": token}
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/login")
def authenticate(auth: Authenticate, db: Session = Depends(get_db)):
    try:
        user = services.authenticate(db=db, email=auth.email, password=auth.password)
        token = create_access_token(user_id=user.id, role_id=user.role.value)
        return token
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/{id}")
def user_detail(id: int, db: Session = Depends(get_db), user=Depends(services.get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        return services.get_user(db=db, id=id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
