import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.session import close_all_sessions

from app.main import app, get_db
from app.api.models import Base


class TestingSession(Session):
    def commit(self):
        # テストなので永続化しない
        self.flush()
        self.expire_all()


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///./test/test.sqlite", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(
        class_=TestingSession, autocommit=False, autoflush=False, bind=engine
    )

    db = TestSessionLocal()

    # sql_app/main.py の get_db() を差し替える
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    def get_db_for_testing():
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            db.rollback()

    app.dependency_overrides[get_db] = get_db_for_testing

    # テストケース実行
    yield db

    # 後処理
    db.rollback()
    close_all_sessions()
    engine.dispose()
