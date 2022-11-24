from sqlalchemy.orm import Session
import numpy as np

from app.models import models
from app.rss.rss import Rss
from app.util.ml_utils import make_dataset_from_db
from app.ml.classifier import Classifier


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
