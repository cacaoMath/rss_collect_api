from sqlalchemy.orm import Session

from . import models, schemas


def get_feed(db: Session, feed_id: int):
    return db.query(models.Feed).filter(models.Feed.id == feed_id).first()


def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feed).offset(skip).limit(limit).all()


def get_feeds_by_url(db: Session, feed_url: str):
    return db.query(models.Feed).filter(models.Feed.url == feed_url).first()


def create_feed(db: Session, feed: schemas.FeedCreate):
    db_feed = models.Feed(url=feed.url, description=feed.description)
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed


def update_feed(db: Session, feed_id: int, feed: schemas.FeedUpdate):
    db_feed = db.query(models.Feed).filter(models.Feed.id == feed_id)
    db_feed.update({
        models.Feed.url: feed.url,
        models.Feed.description: feed.description,
        models.Feed.is_active: feed.is_active
    })
    db.commit()
    return db_feed


def delete_feed(db: Session, feed_id: int):
    db_feed = db.query(models.Feed).filter(models.Feed.id == feed_id)
    db_feed.delete()
    db.commit()
    return {"message": "delete success"}


def get_learning_data(db: Session, data_id: int):
    return db.query(models.LearningData).filter(models.LearningData.id == data_id).first()


def get_all_learning_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LearningData).offset(skip).limit(limit).all()


def create_learning_data(db: Session, learning_data: schemas.LearningDataCreate):
    db_learning_data = models.LearningData(**learning_data.dict())
    db.add(db_learning_data)
    db.commit()
    db.refresh(db_learning_data)
    return db_learning_data
