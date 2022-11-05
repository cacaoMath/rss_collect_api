from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(255), default=False)
    is_active = Column(Boolean, default=True)


class LearningData(Base):
    __tablename__ = "learning_data"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", backref="learning_data")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(10), nullable=False)
