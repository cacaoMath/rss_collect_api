from pydantic.dataclasses import dataclass


@dataclass
class FeedItem:
    title: str
    link: str
    summary: str | None = None
    published: str | None = None
