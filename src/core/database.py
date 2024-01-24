from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.settings import settings

engine = create_engine(settings.postgres_uri)
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    ...
