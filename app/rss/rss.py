import json
import feedparser
import datetime

from ml.classifier import Classifier

rss_url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"
feed = feedparser.parse(rss_url)

print(feed.entries[0])


class Rss():
    def __init__(self):   
        self.today = datetime.date.today()

    def get_feed(self, feed_list: list[dict]) -> list:
        # urlからfeedの内容を取ってくる、取ってきたリストは結合して返す
        pass

    def make_articles(self, collect_articles: list[dict]) -> json:
        # ジャンル分けした記事の一覧を整形して返す
        pass

    def __judge_category(self, content: str) -> list:
        # feedの内容をジャンルに振り分けてリストに出力
        pass

    def __fetch_rss_urls(self) -> list:
        # 登録されているrss feedのurl一覧を返す(is_active = Trueのみ)
        pass
