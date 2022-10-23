from pydantic import BaseModel


class FeedBase(BaseModel):
    url: str
    description: str | None = None


class FeedCreate(FeedBase):
    pass


class Feed(FeedBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class LearningDataBase(BaseModel):
    word: str
    category: str


class LearningDataCreate(LearningDataBase):
    pass


class LearningData(LearningDataBase):
    id: int

    class Config:
        orm_mode = True
