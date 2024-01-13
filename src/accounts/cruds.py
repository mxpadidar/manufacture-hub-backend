from sqlalchemy.orm import Session

from accounts.auth import create_hashed_password, create_token
from accounts.database import UserModel
from accounts.models import User, UserCreate
from core.types import Token, TokenPayload


def get_user_by_email(db: Session, email: str) -> User | None:
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    return User.model_validate(db_user) if db_user else None


def register_user(db: Session, user: UserCreate) -> Token:
    user_data = user.model_dump()
    user_data["password"] = create_hashed_password(user.password)
    user_data["role"] = 1
    user_data["gender"] = 1
    db_user = UserModel(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    payload = TokenPayload(id=db_user.id, role=db_user.role)
    return create_token(payload)
