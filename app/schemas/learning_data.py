from pydantic import BaseModel, Field


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
