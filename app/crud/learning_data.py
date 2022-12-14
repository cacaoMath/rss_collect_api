from sqlalchemy.orm import Session

from app.schemas import learning_data
from app.models import models
from app.crud.category import get_category


def get_learning_data(db: Session, data_id: int):
    return db.query(
        models.LearningData
    ).filter(
        models.LearningData.id == data_id
    ).first()


def get_all_learning_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LearningData).offset(skip).limit(limit).all()


def create_learning_data(db: Session,
                         learning_data: learning_data.LearningDataCreate):
    category = get_category(db=db, category=learning_data.category)
    db_learning_data = models.LearningData(
        word=learning_data.word,
        category_id=category.id
    )
    db.add(db_learning_data)
    db.commit()
    db.refresh(db_learning_data)
    return db_learning_data


def update_learning_data(db: Session, data_id: int,
                         learning_data: learning_data.LearningDataUpdate):
    category = get_category(db=db, category=learning_data.category)
    db_learning_data = db.query(models.LearningData).filter(
        models.LearningData.id == data_id)
    db_learning_data.update({
        models.LearningData.word: learning_data.word,
        models.LearningData.category_id: category.id,
    })
    db.commit()
    return db_learning_data


def delete_learning_data(db: Session, data_id: int):
    db_feed = db.query(models.LearningData).filter(
        models.LearningData.id == data_id)
    db_feed.delete()
    db.commit()
    return {"message": "delete success"}
