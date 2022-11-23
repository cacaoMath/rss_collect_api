from pydantic import BaseModel


class PredictBase(BaseModel):
    text: str


class CollectCategoriesBase(BaseModel):
    categories: list[str]
