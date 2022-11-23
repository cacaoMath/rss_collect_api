from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.crud import (
    feed as feed_crud,
    learning_data as learning_data_crud,
    rss as rss_crud
)
from app.schemas import (
    feed as feed_scm,
    learning_data as learning_data_scm,
    other as other_scm
)
from app.models import models
from app.config import database
from app.ml.classifier import Classifier
from app.util.ml_utils import make_dataset_from_db
from app.util.api_utils import check_credential


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/feeds", response_model=list[feed_scm.Feed])
async def read_feeds(skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    feeds = feed_crud.get_feeds(db, skip=skip, limit=limit)
    return feeds


@app.get("/feeds/{feed_id}", response_model=feed_scm.Feed)
async def read_feed(feed_id: int, db: Session = Depends(get_db)):
    db_feed = feed_crud.get_feed(db, feed_id=feed_id)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="That's feed is not found")
    return db_feed


@app.post("/feeds", response_model=feed_scm.Feed)
def create_feed(feed: feed_scm.FeedCreate,
                db: Session = Depends(get_db),
                cred: bool = Depends(check_credential)):
    db_feed = feed_crud.get_feeds_by_url(db, feed_url=feed.url)
    if db_feed:
        raise HTTPException(
            status_code=400, detail="This RSS feed URL is already registered")
    return feed_crud.create_feed(db, feed)


@app.put("/feeds/{feed_id}")
def update_feed(feed_id: int, feed: feed_scm.FeedUpdate,
                db: Session = Depends(get_db),
                cred: bool = Depends(check_credential)):
    feed_crud.update_feed(db, feed_id, feed)
    return {"message": "success"}


@app.delete("/feeds/{feed_id}")
def delete_feed(feed_id: int,
                db: Session = Depends(get_db),
                cred: bool = Depends(check_credential)):
    return feed_crud.delete_feed(db, feed_id)


@app.get("/learning-data", response_model=list[learning_data_scm.LearningData])
async def read_all_learning_data(skip: int = 0, limit: int = 100,
                                 db: Session = Depends(get_db)):
    return learning_data_crud.get_all_learning_data(db, skip, limit)


@app.get("/learning-data/{data_id}", response_model=learning_data_scm.LearningData)
async def read_learning_data(data_id: int, db: Session = Depends(get_db)):
    return learning_data_crud.get_learning_data(db, data_id)


@app.post("/learning-data", response_model=learning_data_scm.LearningData)
def create_learning_data(learning_data: learning_data_scm.LearningDataCreate,
                         db: Session = Depends(get_db),
                         cred: bool = Depends(check_credential)):
    return learning_data_crud.create_learning_data(db, learning_data)


@app.get("/calassifier")
async def read_classifier():
    return {
        "id": 1,
        "update": "yy:mm:dd:hh:mm:ss"
    }


@app.post("/classifier/predict")
async def classifier_predict(pred: other_scm.PredictBase,
                             db: Session = Depends(get_db),
                             cred: bool = Depends(check_credential)):
    if db.query(models.LearningData.word).count() <= 2:
        raise HTTPException(
            status_code=500,
            detail="Learning data is small. Please input more Learning data"
        )
    classifier = Classifier()
    dataset = make_dataset_from_db(db)
    classifier.train(dataset["word"], dataset["category_id"])
    category = dataset[["category_id", "text"]].drop_duplicates()
    pred = classifier.predict([pred.text])
    return {
        "pred_category":
            category[
                category["category_id"] == pred[0]
            ].iloc[0].text,
        "categories": list(category.text)
    }


@app.post("/rss", response_model=list[feed_scm.FeedItem])
async def read_rss(collect_categories: other_scm.CollectCategoriesBase,
                   db: Session = Depends(get_db)):
    present_categories = rss_crud.get_present_categories(
        db=db, category_list=collect_categories.categories)
    if not len(present_categories):
        raise HTTPException(
            status_code=404, detail="Those coategories are not present.")
    return rss_crud.return_rss_articles(
        db=db,
        collect_categories=present_categories
    )
