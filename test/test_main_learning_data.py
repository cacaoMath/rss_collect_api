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
            "category": {
                "id": 1,
                "text": "fugafuga"
            }
        },
        {
            "id": 2,
            "word": "hogehoge was fugario",
            "category": {
                "id": 2,
                "text": "fugarion"
            }
        },
        {
            "id": 3,
            "word": "hogehoge has fugashi",
            "category": {
                "id": 3,
                "text": "fugashin"
            }
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
        "category": {
            "id": 1,
            "text": "fugafuga"
        }
    }


def test_post_learning_data_認証しないとエラーになるか():
    # 認証しないとpostできない
    response = client.post(
        "/learning-data",
        json={
            "word": "hogerin",
            "category": "hogehoge"
        },
        headers={"Authorization": "Basic dXNlcjppbmF2bGlk=="}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect credentials'}


def test_post_learning_data_データが追加されるか(test_db):
    # データが1つ追加される
    response = client.post(
        "/learning-data",
        json={
            "word": "horerin",
            "category": "hogehoge"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    assert response.json() == {
        "word": "horerin",
        "id": 1,
        "category": {
            "id": 1,
            "text": "hogehoge"
        }
    }
    first_category = test_db.query(Category).filter(
        Category.id == 1).first()
    assert first_category.text == "hogehoge"


def test_post_learning_data_すでに同じCategoryが存在したら同じカテゴリidになる(
        test_db, add_some_learning_data):
    response = client.post(
        "/learning-data",
        json={
            "word": "horerin",
            "category": "fugafuga"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    category_fugafuga = test_db.query(Category).filter(
        Category.text == "fugafuga").first()
    assert response.json()["category"]["id"] == category_fugafuga.id


def test_post_learning_data_同じCategoryが存在しない場合新しいカテゴリを追加する(
        test_db, add_some_learning_data):
    pre_post_category_count = test_db.query(Category).count()
    response = client.post(
        "/learning-data",
        json={
            "word": "horerin",
            "category": "piyopiyo"
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == 200
    after_post_category_count = test_db.query(Category).count()
    assert (after_post_category_count - pre_post_category_count) == 1
    piyopiyo = test_db.query(Category).filter(
        Category.text == "piyopiyo").first()
    assert piyopiyo is not None


@pytest.mark.parametrize(("category", "status"), [
    ("category", 200), ("category-is-work", 200),
    ("category_is_not_work", 422), ("category is not work", 422),
    ("category!is!not!work", 422), ("category@is@not@work", 422),
    ("category~is~not~work", 422), ("category(", 422),
    ("category)", 422), ("categoryああ", 422), ("category\"", 422),
    ("category#", 422), ("category$", 422), ("category%", 422),
    ("category&", 422), ("category'", 422), ("ワーク", 422),
])
def test_post_learning_data_categoryの文字種バリデーション(category, status):
    response = client.post(
        "/learning-data",
        json={
            "word": "word is word",
            "category": category
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status, "categoryはa-z,A-Z,0-9,-のみ"


@pytest.mark.parametrize(("word", "category", "status"), [
    ("a"*255, "category", 200),
    ("a"*1, "category", 200),
    ("word id word", "c"*2, 200),
    ("word id word", "c"*30, 200),
    ("", "category", 422),
    ("a"*256, "category", 422),
    ("word id word", "", 422),
    ("word id word", "c"*31, 422),
])
def test_post_learning_data_wordとcategoryの文字数のバリデーション(word, category, status):
    response = client.post(
        "/learning-data",
        json={
            "word": word,
            "category": category
        },
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    )
    assert response.status_code == status


def test_update_learning_data():
    pass


def test_delete_learning_data_認証しないと削除できない(add_some_learning_data):
    response = client.delete("/learning-data/1")
    assert response.status_code == 401


def test_delete_learning_data_認証情報が違うと削除できない(add_some_learning_data):
    response = client.delete(
        "/learning-data/1",
        headers={"Authorization": "Basic dXNlcjppbmF2bGlk=="})
    assert response.status_code == 401


def test_delete_learning_data_データを削除できる(add_some_learning_data):
    response = client.delete(
        "/learning-data/1",
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
    assert response.json() == {"message": "delete success"}


def test_delete_learning_data_存在しないデータの削除(add_some_learning_data):
    response = client.delete(
        "/feeds/2", headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
