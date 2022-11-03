from fastapi.testclient import TestClient
import pandas as pd

from app.main import app
from app.api.models import LearningData, Feed

client = TestClient(app)


def test_get_feeds_if_feed_is_none():
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == []


def test_get_feeds_if_feed_is_one(test_db):
    test_db.add(
        Feed(
            id=1,
            url="https://example.com/hoge.xml",
            description="hogehoge",
            is_active=True
        )
    )
    test_db.flush()
    test_db.commit()
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == [{
                "url": "https://example.com/hoge.xml",
                "description": "hogehoge",
                "id": 1,
                "is_active": True
            }]


def test_get_feeds_if_feed_is_two(test_db):
    data = [
        Feed(
            id=1,
            url="https://example.com/hoge.xml",
            description="hogehoge",
            is_active=True
        ),
        Feed(
            id=2,
            url="https://example.com/fuga.xml",
            description="fugafuga",
            is_active=False
        )
    ]
    test_db.add_all(data)
    test_db.flush()
    test_db.commit()
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == [{
                "url": "https://example.com/hoge.xml",
                "description": "hogehoge",
                "id": 1,
                "is_active": True
            },
            {
                "url": "https://example.com/fuga.xml",
                "description": "fugafuga",
                "id": 2,
                "is_active": False
            }]


def test_get_feed(test_db):
    test_db.add(
        Feed(
            id=1,
            url="https://example.com/hoge.xml",
            description="hogehoge",
            is_active=True
        )
    )
    test_db.flush()
    test_db.commit()
    response = client.get("/feeds/1")
    assert response.status_code == 200
    assert response.json() == {
            "url": "https://example.com/hoge.xml",
            "description": "hogehoge",
            "id": 1,
            "is_active": True
        }


def test_classifier_predict_if_learning_data_is_few(test_db):
    test_db.add(LearningData(word="hogehoge", category="fugafuga"))
    test_db.commit()
    response = client.post("/classifier/predict", json={"text": "test"})
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Learning data is small. Please input more Learning data"
    }
    LearningData(word="piyopiyo", category="kogekoge")
    test_db.commit()
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Learning data is small. Please input more Learning data"
    }


def test_classifier_predict_if_learning_data_is_three(test_db, mocker):
    data = [
        LearningData(word="hogehoge is fugafuga", category="fugafuga"),
        LearningData(word="hogehoge was fugario", category="fugafuga"),
        LearningData(word="hogehoge has fugashi", category="fugafuga")
    ]
    test_db.add_all(data)
    test_db.flush()
    test_db.commit()
    # テスト時はdbが永続化されず、空になるのでmockで対応
    mocker.patch(
        "app.main.pd.read_sql_query",
        return_value=pd.DataFrame(
            {
                "word": [d.word for d in data],
                "category": [d.category for d in data]
            }
        )
    )
    response = client.post("/classifier/predict", json={"text": "test"})
    assert response.status_code == 200
    assert response.json() == {
        "pred_category": "fugafuga",
        "categories": "['fugafuga']"
    }
