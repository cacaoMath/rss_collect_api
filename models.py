from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(255), default=False)
    is_active = Column(Boolean, default=True)


class LearnigData(Base):
    __tablename__ = "learning_data"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), index=True, nullable=False)
    category = Column(String(10), nullable=False)
