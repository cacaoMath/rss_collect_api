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
    category = get_category(db=db, category=learning_data.category)
    db_learning_data = models.LearningData(
        word=learning_data.word,
        category_id=category.id
    )
    db.add(db_learning_data)
    db.commit()
    db.refresh(db_learning_data)
    return db_learning_data


def get_category(db: Session, category: str):
    is_category = db.query(models.Category).filter(
            models.Category.text == category
        ).first()
    return is_category if is_category is not None else create_category(db, category)


def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(text=category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
