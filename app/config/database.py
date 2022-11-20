from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.env import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_SERVER,
    POSTGRES_SERVER_PORT,
)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/my_rss_api.sqlite"
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_SERVER_PORT,
    POSTGRES_DB)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
