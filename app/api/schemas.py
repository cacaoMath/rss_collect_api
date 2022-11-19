from pydantic import BaseModel, Field


class FeedBase(BaseModel):
    url: str
    description: str | None = Field(
        default=None,
        title="RSS feed description",
        max_length=255
    )


class FeedCreate(FeedBase):
    url: str = Field(
        title="RSS feed URL",
        max_length=255,
        # https://uibakery.io/regex-library/url-regex-python 参考
        regex="^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    )


class FeedUpdate(FeedCreate):
    is_active: bool


class Feed(FeedBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class LearningDataBase(BaseModel):
    word: str = Field(
        title="Category name",
        min_length=1,
        max_length=255,
    )


class LearningDataCreate(LearningDataBase):
    category: str = Field(
        title="Category name",
        min_length=1,
        max_length=30,
        regex="^[a-zA-z0-9-].+$"  # categoryはa-z,A-Z,0-9,-のみ使用可とする
    )


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


class CollectCategoriesBase(BaseModel):
    categories: list[str]
