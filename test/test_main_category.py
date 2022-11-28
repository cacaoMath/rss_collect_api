from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.models.models import Category

client = TestClient(app)


@pytest.fixture
def add_some_category(test_db):
    catefory_data = [
        Category(text="fugafuga"),
        Category(text="fugarion"),
        Category(text="fugashin")
    ]
    test_db.add_all(catefory_data)
    test_db.commit()


def test_get_categories_カテゴリが無い場合空リストが返る():
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == []


def test_get_categories_カテゴリ一覧が返ってくる(add_some_category):
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == [
        {
            "text": "fugafuga",
            "id": 1
        },
        {
            "text": "fugarion",
            "id": 2
        },
        {
            "text": "fugashin",
            "id": 3
        }
    ]


def test_get_categories_100件まで返ってくる(test_db):
    data = []
    for i in range(100):
        data.append(Category(text="a"*i))
    test_db.add_all(data)
    test_db.commit()
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) == 100
    test_db.add(Category(text="b"))
    test_db.commit()
    assert response.status_code == 200
    assert len(response.json()) == 100
