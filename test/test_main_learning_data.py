import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.models import Category, LearningData

client = TestClient(app)


@pytest.fixture
def add_some_learning_data(test_db):
    catefory_data = [
        Category(text="fugafuga"),
        Category(text="fugarion"),
        Category(text="fugashin")
    ]
    test_db.add_all(catefory_data)
    test_db.commit()
    fixture_data = [
        LearningData(word="hogehoge is fugafuga",
                     category_id=catefory_data[0].id),
        LearningData(word="hogehoge was fugario",
                     category_id=catefory_data[1].id),
        LearningData(word="hogehoge has fugashi",
                     category_id=catefory_data[2].id)
    ]
    test_db.add_all(fixture_data)
    test_db.commit()


def test_get_learning_data_all_データがない時は空リストを返す():
    response = client.get("/learning-data")
    assert response.json() == []


def test_get_learning_data_all_全てのデータを返す(add_some_learning_data):
    response = client.get("/learning-data")
    assert response.json() == [
        {
            "id": 1,
            "word": "hogehoge is fugafuga",
                    "category_id": 1
        },
        {
            "id": 2,
            "word": "hogehoge was fugario",
            "category_id": 2
        },
        {
            "id": 3,
            "word": "hogehoge has fugashi",
            "category_id": 3
        }
    ]


def test_get_a_lerning_deta_存在しないデータを選んだら404を返す(add_some_learning_data):
    response = client.get("/learning-data/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "That's learning data is not found"}


def test_get_a_lerning_deta_指定したデータが返ってくる(add_some_learning_data):
    response = client.get("/learning-data/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "word": "hogehoge is fugafuga",
        "category_id": 1,
    }
