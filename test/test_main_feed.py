from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Feed
import pytest

client = TestClient(app)


@pytest.fixture
def test_add_a_feed(test_db):
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


def test_get_feeds_if_feed_is_one(test_add_a_feed):
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


def test_get_feed_存在するidを指定する(test_add_a_feed):
    response = client.get("/feeds/1")
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://example.com/hoge.xml",
        "description": "hogehoge",
        "id": 1,
        "is_active": True
    }


def test_get_feed_存在しないidを指定する(test_add_a_feed):
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


def test_post_feed_データが追加されるか(auth_ok):
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


def test_post_feed_すでに同じURLが存在したら登録できない(auth_ok, test_add_a_feed):
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


def test_post_feed_descriptionは空でも登録可(auth_ok):
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


def test_post_feed_URLでないものはvalidation_error(auth_ok):
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
def test_post_feed_URLとdescriptionのバリデーション(auth_ok, url, description, status):
    response = client.post(
        "/feeds",
        json={
            "url": url,
            "description": description
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status


def test_update_feed():
    pass


def test_delete_feed_認証しないと削除できない(test_add_a_feed):
    response = client.delete("/feeds/1")
    assert response.status_code == 401


def test_delete_feed_データを削除できる(auth_ok, test_add_a_feed):
    response = client.delete(
        "/feeds/1", headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
    assert response.json() == {"message": "delete success"}


def test_delete_feed_存在しないデータの削除(auth_ok, test_add_a_feed):
    response = client.delete(
        "/feeds/2", headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
