from fastapi.testclient import TestClient
import pandas as pd
from app.main import app
from app.db.models import LearningData, Category, Feed

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


def test_classifier_predict_if_learning_data_is_few(test_db, mocker):
    category = Category(text="fugafuga")
    test_db.add(category)
    test_db.commit()
    test_db.add(LearningData(word="運転したくないなという", category_id=category.id))
    test_db.commit()
    mocker.patch("secrets.compare_digest", result_value=True)
    response = client.post(
        "/classifier/predict",
        json={"text": "test"},
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Learning data is small. Please input more Learning data"
    }
    # 2が境界値
    test_db.add(Category(text="fugafuga"))
    test_db.commit()
    test_db.add(LearningData(word="私は車に乗ります", category_id=category.id))
    test_db.commit()
    response = client.post(
        "/classifier/predict",
        json={"text": "test"},
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Learning data is small. Please input more Learning data"
    }


def test_classifier_predict_if_learning_data_is_three(test_db, mocker):
    category = Category(text="fugafuga")
    test_db.add(category)
    test_db.commit()
    data = [
        LearningData(word="hogehoge is fugafuga", category_id=category.id),
        LearningData(word="hogehoge was fugario", category_id=category.id),
        LearningData(word="hogehoge has fugashi", category_id=category.id)
    ]
    test_db.add_all(data)
    test_db.commit()
    # テスト時はdbが永続化されず、空になるのでmockで対応
    mocker.patch(
        "app.main.make_dataset_from_db",
        return_value=pd.DataFrame(
            {
                "word": [d.word for d in data],
                "category_id": [d.category_id for d in data],
                "text": [d.category.text for d in data]
            }
        )
    )
    mocker.patch("secrets.compare_digest", result_value=True)
    response = client.post(
        "/classifier/predict",
        json={"text": "test"},
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {
        "pred_category": "fugafuga",
        "categories": ["fugafuga"]
    }


def test_read_rss_(test_db, mocker):
    category = Category(text="fugafuga")
    test_db.add(category)
    test_db.commit()
    data = [
        LearningData(word="hogehoge is fugafuga", category_id=category.id),
        LearningData(word="hogehoge was fugario", category_id=category.id),
        LearningData(word="hogehoge has fugashi", category_id=category.id)
    ]
    test_db.add_all(data)
    feed = Feed(url="test/rss/resource/rss_a.xml")
    test_db.add(feed)
    test_db.commit()
    # テスト時はdbが永続化されず、空になるのでmockで対応
    mocker.patch(
        "app.api.crud.make_dataset_from_db",
        return_value=pd.DataFrame(
            {
                "word": [d.word for d in data],
                "category_id": [d.category_id for d in data],
                "text": [d.category.text for d in data]
            }
        )
    )
    mocker.patch("secrets.compare_digest", result_value=True)
    response = client.post(
        "/rss",
        json={"categories": ["mogamoga"]},
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Those coategories are not present."
    }, "存在しないカテゴリでも404がかえってないよ"
    response = client.post(
        "/rss",
        json={"categories": ["fugafuga"]},
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            'title': 'aaaa',
            'link': 'https://aaa.co.jp/aaa.html',
            'published': 'Fri, 04 Nov 2022 09:40:00 +0900',
            'summary': 'hugahuga',
        },
        {
            'title': 'bbbb',
            'link': 'https://bbb.co.jp/bbb.html',
            'published': 'Wed, 02 Nov 2022 07:00:00 +0900',
            'summary': 'hogehoge',
        },
        {
            'title': 'cccc',
            'link': 'https://ccc.co.jp/ccc.html',
            'published': 'Tue, 01 Nov 2022 11:42:00 +0900',
            'summary': 'kogekoge',
        },
    ], "返す値がおかしいよ！"
