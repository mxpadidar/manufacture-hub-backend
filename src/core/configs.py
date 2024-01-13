from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.envs import envs
from core.types import JwtConfigs

engine = create_engine(envs.postgres_uri)
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


jwt_configs = JwtConfigs(
    secret=envs.secret_key, algorithm=envs.jwt_algorithm, expires_in=envs.jwt_expires_in
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
