import json
import feedparser
import datetime
from app.util.type import FeedItem


class Rss():
    def __init__(self):
        self.today = datetime.date.today()

    # urlからfeedの内容を取ってくる、取ってきたリストは結合して返す
    def get_feed(self, feed_url_list: list[str]) -> list[FeedItem]:
        if not feed_url_list:
            return []
        feed_list = self.__feedparser(feed_url_list)
        tmp_list = []
        for feed in feed_list:
            for entry in feed.entries:
                tmp_list.append(
                    FeedItem(
                        title=entry.title,
                        link=entry.link,
                        summary=entry.summary,
                        published=entry.published
                    )
                )
        return tmp_list

    def make_articles(self, collect_articles: list[dict]) -> json:
        # ジャンル分けした記事の一覧を整形して返す
        pass

    def __feedparser(self, url_list: list[str]):
        return list(map(feedparser.parse, url_list))
