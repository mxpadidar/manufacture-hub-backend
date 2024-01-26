from sqlalchemy.orm import Session

from core.db import session_maker


def get_db():
    db: Session = session_maker()
    try:
        yield db
    finally:
        db.close()
