from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.api import crud, models, schemas
from app.db.database import SessionLocal, engine
from app.ml.classifier import Classifier
from app.util.ml_utils import make_van_list

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
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
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db)):
    db_feed = crud.get_feeds_by_url(db, feed_url=feed.url)
    if db_feed:
        raise HTTPException(status_code=400, detail="This RSS feed URL is already registered")
    return crud.create_feed(db, feed)


@app.put("/feeds/{feed_id}")
def update_feed(feed_id: int, feed: schemas.FeedUpdate, db: Session = Depends(get_db)):
    crud.update_feed(db, feed_id, feed)
    return {"message": "success"}


@app.delete("/feeds/{feed_id}")
def delete_feed(feed_id: int, db: Session = Depends(get_db)):
    return crud.delete_feed(db, feed_id)


@app.get("/learning-data", response_model=list[schemas.LearningData])
async def read_all_learning_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_learning_data(db, skip, limit)


@app.get("/learning-data/{data_id}", response_model=schemas.LearningData)
async def read_learning_data(data_id: int, db: Session = Depends(get_db)):
    return crud.get_learning_data(db, data_id)


@app.post("/learning-data", response_model=schemas.LearningData)
def create_learning_data(learning_data: schemas.LearningDataCreate, db: Session = Depends(get_db)):
    return crud.create_learning_data(db, learning_data)


@app.get("/calassifier")
async def read_classifier():
    return {
        "id": 1,
        "update": "yy:mm:dd:hh:mm:ss"
    }


@app.post("/classifier/predict")
async def rclassifier_predict(pred: schemas.PredictBase):
    dataset = pd.read_sql_query(sql="SELECT word, category FROM learning_data", con=engine)
    classifier = Classifier()
    # カテゴリを数値化
    dataset["y"], category = pd.factorize(dataset["category"])
    dataset["word"] = dataset["word"].apply(make_van_list)
    classifier.train(dataset["word"], dataset["y"])
    pred = classifier.predict([pred.text])
    categories = category.values
    return {
        "pred_category": str(categories[pred[0]]),
        "categories": str(categories)
    }


@app.get("/rss")
async def read_rss():
    return {
        [
            {
                "id": 1,
                "title": "aaa",
                "URL": "https://bbb.com"
            },
            {
                "id": 2,
                "title": "aaa",
                "URL": "https://bbb.com"
            },
        ]
    }
