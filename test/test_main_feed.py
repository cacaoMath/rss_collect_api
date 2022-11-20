from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Feed
import pytest

client = TestClient(app)


def test_get_feeds_if_feed_is_none(test_db):
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


def test_post_feed_認証しないとエラーになるか(test_db, mocker):
    # 認証しないとpostできない
    response = client.post(
        "/feeds",
        json={
            "url": "http://abc.com/def.xml",
            "description": "abc rss"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect credentials'}


def test_post_feed_データが追加されるか(test_db, mocker):
    # データが1つ追加される
    mocker.patch("secrets.compare_digest", result_value=True)
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


def test_post_feed_すでに同じURLが存在したら登録できない(test_db, mocker):
    mocker.patch("secrets.compare_digest", result_value=True)
    test_db.add(
        Feed(
            id=1,
            url="http://abc.com/def.xml",
            description="abc rss",
            is_active=True
        )
    )
    test_db.flush()
    test_db.commit()
    response = client.post(
        "/feeds",
        json={
            "url": "http://abc.com/def.xml",
            "description": "abc rss"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'This RSS feed URL is already registered'}


def test_post_feed_descriptionは空でも登録可(test_db, mocker):
    mocker.patch("secrets.compare_digest", result_value=True)
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


def test_post_feed_URLでないものはvalidation_error(test_db, mocker):
    mocker.patch("secrets.compare_digest", result_value=True)
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
def test_post_feed_URLとdescriptionのバリデーション(
        test_db, mocker, url, description, status):
    mocker.patch("secrets.compare_digest", result_value=True)
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


def test_delete_feed():
    pass
