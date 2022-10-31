from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.api.models import LearningData
from test.fixture_db import test_db

client = TestClient(app)


def test_get_feeds_if_feed_is_none(mocker):
    mocker.patch("app.main.crud.get_feeds", return_value=[])
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == []


def test_get_feeds_if_feed_is_one(mocker):
    mocker.patch(
        "app.main.crud.get_feeds",
        return_value=[{
              "url": "https://example.com/hoge.xml",
              "description": "hogehoge",
              "id": 1,
              "is_active": True
            }]
    )
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == [{
              "url": "https://example.com/hoge.xml",
              "description": "hogehoge",
              "id": 1,
              "is_active": True
            }]


def test_get_feeds_if_feed_is_two(mocker):
    mocker.patch(
        "app.main.crud.get_feeds",
        return_value=[{
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
    )
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


def test_get_feed(mocker):
    mocker.patch(
        "app.main.crud.get_feed",
        return_value={
            "url": "https://example.com/hoge.xml",
            "description": "hogehoge",
            "id": 1,
            "is_active": True
        }
    )
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
    test_db.flush()
    test_db.commit()
    response = client.post("/classifier/predict", json={"text": "test"})
    assert response.status_code == 500
    assert response.json() == {
      "detail": "Learning data is small. Please input more Learning data"
    }
    LearningData(word="piyopiyo", category="kogekoge")
    test_db.flush()
    test_db.commit()
    assert response.status_code == 500
    assert response.json() == {
      "detail": "Learning data is small. Please input more Learning data"
    }

@pytest.mark.skip # dbの設定がうまくいかないのでpending
def test_classifier_predict_if_learning_data_is_three(test_db):
    data = [
        LearningData(word="hogehoge", category="fugafuga"),
        LearningData(word="hogehoge", category="fugafuga"),
        LearningData(word="hogehoge", category="fugafuga")
    ]
    test_db.add_all(data)
    test_db.flush()
    test_db.commit()
    response = client.post("/classifier/predict", json={"text": "test"})
    assert response.status_code == 200
