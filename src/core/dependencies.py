from sqlalchemy.orm import Session

from core.database import SessionFactory


def get_db():
    db: Session = SessionFactory()
    try:
        yield db
    finally:
        db.close()
