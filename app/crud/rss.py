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
    category_value_list = db.query(models.Category.id).filter(
        models.Category.text.in_(collect_categories)).all()
    rss = Rss()
    feed_url_list = [
        "http://127.0.0.1:9000/feeds/feeds/002.xml",
        "http://127.0.0.1:9000/feeds/feeds/003.xml",
        "http://127.0.0.1:9000/feeds/feeds/001.xml",
        "http://127.0.0.1:9000/feeds/feeds/004.xml",
        "http://127.0.0.1:9000/feeds/feeds/005.xml",
        "http://127.0.0.1:9000/feeds/feeds/006.xml",
        "http://127.0.0.1:9000/feeds/feeds/007.xml",
        "http://127.0.0.1:9000/feeds/feeds/008.xml",
        "http://127.0.0.1:9000/feeds/feeds/009.xml",
        "http://127.0.0.1:9000/feeds/feeds/010.xml",
        "http://127.0.0.1:9000/feeds/feeds/011.xml",
        "http://127.0.0.1:9000/feeds/feeds/012.xml",
        "http://127.0.0.1:9000/feeds/feeds/013.xml",
        "http://127.0.0.1:9000/feeds/feeds/014.xml",
        "http://127.0.0.1:9000/feeds/feeds/015.xml",
        "http://127.0.0.1:9000/feeds/feeds/016.xml",
        "http://127.0.0.1:9000/feeds/feeds/017.xml",
        "http://127.0.0.1:9000/feeds/feeds/018.xml",
        "http://127.0.0.1:9000/feeds/feeds/019.xml"
    ]
    # feed_url_list = [elm[0] for elm in db.query(models.Feed.url).all()]
    feed_list = rss.get_feed(feed_url_list=feed_url_list)
    return rss.make_articles(
        feed_list=feed_list,
        category_value_list=np.array([c[0] for c in category_value_list]),
        classifier=classifier
    )


def get_present_categories(db: Session, category_list: list[str]) -> list[str]:
    categories = db.query(models.Category.text).all()
    categories = [category[0] for category in categories]
    return list(set(category_list) & set(categories))
