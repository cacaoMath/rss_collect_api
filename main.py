from fastapi import FastAPI

app = FastAPI()


@app.get("/feeds")
async def read_feeds():
    return {
        "id":   1,
        "URL":  "https://cacaomath.com"
    }


@app.get("/feeds/{feed_id}")
async def read_feed(feed_id: int):
    return {
        "id":   feed_id,
        "URL":  "https://cacaomath.com"
    }


@app.get("/learning-data")
async def read_all_learning_data():
    return {
        [
            {
                "id": 1,
                "word": "aaa",
                "category": "bbb"
            },
        ]
    }


@app.get("/learning-data/{data_id}")
async def read_learning_data(data_id: int):
    return {
        "id": data_id,
        "word": "aaa",
        "category": "bbb"
    }


@app.get("/calassifier")
async def read_classifier():
    return {
        "id": 1,
        "update": "yy:mm:dd:hh:mm:ss"
    }


@app.get("/calassifier/learn")
async def learn_classifier():
    return {
        "message": "learning..."
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
