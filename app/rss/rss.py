import feedparser
import datetime
import numpy as np

from app.util.type import FeedItem
from app.ml.classifier import Classifier


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

    # 自分が決めたジャンルの記事を集める
    # classifierはfit後を入れる
    def make_articles(self, feed_list: list[FeedItem], category_value_list: np.ndarray, classifier: Classifier) -> list[FeedItem]:
        title_list = [item.title for item in feed_list]
        pred_list = classifier.predict(title_list)
        pred_mask = np.isin(pred_list, category_value_list)
        select_feed_list = np.array(feed_list)[pred_mask].tolist()
        return list(map(lambda x: x, select_feed_list))

    def __feedparser(self, url_list: list[str]) -> list:
        return list(map(feedparser.parse, url_list))
