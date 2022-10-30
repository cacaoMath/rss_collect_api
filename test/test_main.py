from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_feeds_if_feed_is_none(mocker):
    mocker.patch("main.crud.get_feeds", return_value=[])
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == []


def test_get_feeds_if_feed_is_one(mocker):
    mocker.patch(
        "main.crud.get_feeds",
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
        "main.crud.get_feeds",
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
        "main.crud.get_feed",
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