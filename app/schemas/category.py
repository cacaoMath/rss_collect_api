from pydantic import BaseModel


class CategoryBase(BaseModel):
    text: str


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
