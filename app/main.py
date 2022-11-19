from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api import crud, schemas
from app.db import database, models
from app.ml.classifier import Classifier
from app.util.ml_utils import make_dataset_from_db
from app.util.api_utils import check_credential
from app.util.type import FeedItem

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/feeds", response_model=list[schemas.Feed])
async def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = crud.get_feeds(db, skip=skip, limit=limit)
    return feeds


@app.get("/feeds/{feed_id}", response_model=schemas.Feed)
async def read_feed(feed_id: int, db: Session = Depends(get_db)):
    db_feed = crud.get_feed(db, feed_id=feed_id)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="That's feed is not found")
    return db_feed


@app.post("/feeds", response_model=schemas.Feed)
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
    db_feed = crud.get_feeds_by_url(db, feed_url=feed.url)
    if db_feed:
        raise HTTPException(
            status_code=400, detail="This RSS feed URL is already registered")
    return crud.create_feed(db, feed)


@app.put("/feeds/{feed_id}")
def update_feed(feed_id: int, feed: schemas.FeedUpdate, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
    crud.update_feed(db, feed_id, feed)
    return {"message": "success"}


@app.delete("/feeds/{feed_id}")
def delete_feed(feed_id: int, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
    return crud.delete_feed(db, feed_id)


@app.get("/learning-data", response_model=list[schemas.LearningData])
async def read_all_learning_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_learning_data(db, skip, limit)


@app.get("/learning-data/{data_id}", response_model=schemas.LearningData)
async def read_learning_data(data_id: int, db: Session = Depends(get_db)):
    return crud.get_learning_data(db, data_id)


@app.post("/learning-data", response_model=schemas.LearningData)
def create_learning_data(learning_data: schemas.LearningDataCreate, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
    return crud.create_learning_data(db, learning_data)


@app.get("/calassifier")
async def read_classifier():
    return {
        "id": 1,
        "update": "yy:mm:dd:hh:mm:ss"
    }


@app.post("/classifier/predict")
async def classifier_predict(pred: schemas.PredictBase, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
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


@app.post("/rss", response_model=list[FeedItem])
async def read_rss(collect_categories: schemas.CollectCategoriesBase, db: Session = Depends(get_db)):
    present_categories = crud.get_present_categories(
        db=db, category_list=collect_categories.categories)
    if not len(present_categories):
        raise HTTPException(
            status_code=404, detail="Those coategories are not present.")
    return crud.return_rss_articles(
        db=db,
        collect_categories=present_categories
    )
