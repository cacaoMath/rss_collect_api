from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Feed
import pytest

client = TestClient(app)


@pytest.fixture
def add_a_feed_data(test_db):
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


def test_get_feeds_if_feed_is_none():
    response = client.get("/feeds")
    assert response.status_code == 200
    assert response.json() == []


def test_get_feeds_if_feed_is_one(add_a_feed_data):
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


def test_get_feed_存在するidを指定する(add_a_feed_data):
    response = client.get("/feeds/1")
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://example.com/hoge.xml",
        "description": "hogehoge",
        "id": 1,
        "is_active": True
    }


def test_get_feed_存在しないidを指定する(add_a_feed_data):
    response = client.get("/feeds/2")
    assert response.status_code == 404


def test_post_feed_認証しないとエラーになるか():
    # 認証しないとpostできない
    response = client.post(
        "/feeds",
        json={
            "url": "http://abc.com/def.xml",
            "description": "abc rss"
        },
        headers={"Authorization": "Basic dXNlcjppbmF2bGlk=="}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect credentials'}


def test_post_feed_データが追加されるか():
    # データが1つ追加される
    response = client.post(
        "/feeds",
        json={
            "url": "http://abc.com/def.xml",
            "description": "abc rss"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": "http://abc.com/def.xml",
        "description": "abc rss",
        "id": 1,
        "is_active": True
    }


def test_post_feed_すでに同じURLが存在したら登録できない(add_a_feed_data):
    response = client.post(
        "/feeds",
        json={
            "url": "https://example.com/hoge.xml",
            "description": "hogehoge"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'This RSS feed URL is already registered'}


def test_post_feed_descriptionは空でも登録可():
    # descriptionが空でもいい
    response = client.post(
        "/feeds",
        json={
            "url": "http://ghi.com/jkl.xml",
            "description": ""
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": "http://ghi.com/jkl.xml",
        "description": "",
        "id": 1,
        "is_active": True
    }


def test_post_feed_URLでないものはvalidation_error():
    # URLでないものはvalidation error
    response = client.post(
        "/feeds",
        json={
            "url": "🥺エラーだよ",
            "description": ""
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 422, "validationがおかしいよ"


@pytest.mark.parametrize(("url", "description", "status"), [
    ("https://ac.com/"+"a"*240, "", 200),
    ("https://ac.com/"+"a"*241, "", 422),
    ("https://ac.com", "a"*255, 200),
    ("https://ac.com", "a"*256, 422),
])
def test_post_feed_URLとdescriptionのバリデーション(url, description, status):
    response = client.post(
        "/feeds",
        json={
            "url": url,
            "description": description
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status


def test_update_feed_認証しないと更新できない(add_a_feed_data):
    response = client.put(
        "/feeds/1",
        json={
            "url": "https://abc.com",
            "description": "update",
            "is_active": True
        }
    )
    assert response.status_code == 401


def test_update_feed_データの更新ができる(add_a_feed_data, test_db):
    response = client.put(
        "/feeds/1",
        json={
            "url": "https://abc.com",
            "description": "update",
            "is_active": False
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "success"}
    first_feed = test_db.query(Feed).filter(Feed.id == 1).first()
    assert first_feed.url == "https://abc.com"
    assert first_feed.description == "update"
    assert first_feed.is_active is False


def test_update_feed_すでに同じURLが存在したら更新できない(add_a_feed_data):
    response = client.put(
        "/feeds/1",
        json={
            "url": "https://example.com/hoge.xml",
            "description": "hogehoge",
            "is_active": True
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'This RSS feed URL is already registered'}


def test_update_feed_descriptionは空でも更新可(add_a_feed_data, test_db):
    # descriptionが空でもいい
    response = client.put(
        "/feeds/1",
        json={
            "url": "http://ghi.com/jkl.xml",
            "description": "",
            "is_active": True
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "success"}
    first_feed = test_db.query(Feed).filter(Feed.id == 1).first()
    assert first_feed.url == "http://ghi.com/jkl.xml"
    assert first_feed.description == ""
    assert first_feed.is_active is True


def test_update_feed_URLでないものはvalidation_error(add_a_feed_data):
    # URLでないものはvalidation error
    response = client.put(
        "/feeds/1",
        json={
            "url": "🥺エラーだよ",
            "description": "",
            "is_active": True
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 422, "validationがおかしいよ"


@pytest.mark.parametrize(("url", "description", "status"), [
    ("https://ac.com/"+"a"*240, "", 200),
    ("https://ac.com/"+"a"*241, "", 422),
    ("https://ac.com", "a"*255, 200),
    ("https://ac.com", "a"*256, 422),
])
def test_update_feed_URLとdescriptionのバリデーション(url, description, status):
    response = client.put(
        "/feeds/1",
        json={
            "url": url,
            "description": description,
            "is_active": True
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status


@pytest.mark.parametrize(("is_active", "status"), [
    (True, 200),
    (False, 200),
])
def test_update_feed_is_activeが更新できるか(is_active, status):
    response = client.put(
        "/feeds/1",
        json={
            "url": "https://abc.com",
            "description": "update",
            "is_active": is_active
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status


def test_delete_feed_認証しないと削除できない(add_a_feed_data):
    response = client.delete("/feeds/1")
    assert response.status_code == 401


def test_delete_feed_データを削除できる(add_a_feed_data):
    response = client.delete(
        "/feeds/1", headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
    assert response.json() == {"message": "delete success"}


def test_delete_feed_存在しないデータの削除(add_a_feed_data):
    response = client.delete(
        "/feeds/2", headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
