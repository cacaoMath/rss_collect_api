from sqlalchemy.orm import Session
import numpy as np

from . import models, schemas
from app.rss.rss import Rss
from app.util.ml_utils import make_dataset_from_db
from app.ml.classifier import Classifier


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


def return_rss_articles(db: Session, collect_categories: list[str]):
    dataset = make_dataset_from_db(db)
    classifier = Classifier()
    classifier.train(dataset["word"], dataset["category_id"])
    category = db.query(models.Category).all()
    category = np.array([[int(elm.id), str(elm.text)] for elm in category])
    # 指定したカテゴリの値分だけ残すようにマスキング
    mask = np.isin(category[:, 1], collect_categories)
    # numpy strのndarrayになっているのでintにする
    collect_value_list = category[:, 0][mask].astype(np.int64)
    rss = Rss()
    feed_url_list = db.query(models.Feed.url).all()
    feed_url_list = np.array(feed_url_list)[:, 0].tolist()
    feed_list = rss.get_feed(feed_url_list=feed_url_list)
    return rss.make_articles(
        feed_list=feed_list,
        category_value_list=collect_value_list,
        classifier=classifier
    )


def get_present_categories(db: Session, category_list: list[str]) -> list[str]:
    categories = db.query(models.Category.text).all()
    categories = [category[0] for category in categories]
    return list(set(category_list) & set(categories))
