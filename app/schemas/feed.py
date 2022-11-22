from pydantic.dataclasses import dataclass
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
        regex="^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"  # noqa: E501
    )


class FeedUpdate(FeedCreate):
    is_active: bool


class Feed(FeedBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


@dataclass
class FeedItem:
    title: str
    link: str
    summary: str | None = None
    published: str | None = None
