from pydantic import BaseModel


class FeedBase(BaseModel):
    url: str
    description: str | None = None


class FeedCreate(FeedBase):
    pass


class FeedUpdate(FeedBase):
    url: str
    description: str | None = None
    is_active: bool


class Feed(FeedBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class LearningDataBase(BaseModel):
    word: str


class LearningDataCreate(LearningDataBase):
    category: str


class LearningData(LearningDataBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    text: str


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class PredictBase(BaseModel):
    text: str
