from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import numpy as np

from app.api import crud, models, schemas
from app.db.database import SessionLocal, engine
from app.ml.classifier import Classifier
from app.rss.rss import Rss
from app.util.ml_utils import make_dataset_from_db
from app.util.api_utils import check_credential

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
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db), cred: bool = Depends(check_credential)):
    db_feed = crud.get_feeds_by_url(db, feed_url=feed.url)
    if db_feed:
        raise HTTPException(status_code=400, detail="This RSS feed URL is already registered")
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
        raise HTTPException(status_code=500, detail="Learning data is small. Please input more Learning data")
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


@app.post("/rss")
async def read_rss(collect_categories: schemas.CollectCategoriesBase, db: Session = Depends(get_db)):
    collect_categories = collect_categories.categories
    dataset = make_dataset_from_db(db)
    classifier = Classifier()
    classifier.train(dataset["word"], dataset["category_id"])
    category = dataset[["category_id", "text"]].drop_duplicates().to_numpy()
    # 指定したカテゴリの値分だけ残すようにマスキング
    mask = np.isin(category[:, 1], collect_categories)
    collect_value_list = category[:, 0][mask]
    rss = Rss()
    feed_url_list = db.query(models.Feed.url).all()
    feed_url_list = np.array(feed_url_list)[:, 0].tolist()
    feed_list = rss.get_feed(feed_url_list=feed_url_list)
    result = rss.make_articles(
            feed_list=feed_list,
            category_value_list=collect_value_list,
            classifier=classifier
        )
    return result
