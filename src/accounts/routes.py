from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from accounts import services
from accounts.models import UserCreate
from core.dependencies import get_db
from core.types import TokenPayload

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register")
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return services.user_register(user=user, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
def user_detail(id: int, db: Session = Depends(get_db)):
    try:
        user = services.user_details(db=db, id=id)
        payload = TokenPayload(id=user.id, role=user.role.value)
        token = services.create_token(payload=payload)
        return {"user": user, "token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
