from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.configs import configs

default_engine = create_engine(configs.database_url)
SessionFactory = sessionmaker(bind=default_engine, autocommit=False, autoflush=False)
ModelBase = declarative_base()
