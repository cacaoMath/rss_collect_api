from sqlalchemy.orm import Session

from app.schemas import schemas
from app.models import models


def get_category(db: Session, category: str):
    is_category = db.query(models.Category).filter(
        models.Category.text == category
    ).first()
    return is_category if is_category is not None else create_category(
        db, category
    )


def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(text=category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
