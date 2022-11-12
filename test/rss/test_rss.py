from app.rss.rss import Rss, FeedItem

rss = Rss()


def test_Rss_get_feed_if_feed_url_is_none():
    url_list = []
    assert rss.get_feed(feed_url_list=url_list) == [], "空リストがかえってくること"


def test_Rss_get_feed_if_feed_url_is_any():
    # testではローカルのxmlでfeedparserを使う
    url_list = [
        "test/rss/resource/rss_a.xml",
        "test/rss/resource/rss_a.xml"
    ]
    result = rss.get_feed(feed_url_list=url_list)
    right_result = [
        FeedItem(
            title="aaaa",
            link="https://aaa.co.jp/aaa.html",
            summary="hugahuga",
            published="Fri, 04 Nov 2022 09:40:00 +0900"
        ),
        FeedItem(
            title="bbbb",
            link="https://bbb.co.jp/bbb.html",
            summary="hogehoge",
            published="Wed, 02 Nov 2022 07:00:00 +0900"
        ),
        FeedItem(
            title="cccc",
            link="https://ccc.co.jp/ccc.html",
            summary="kogekoge",
            published="Tue, 01 Nov 2022 11:42:00 +0900"
        ),
    ]
    assert result == right_result*2, "2つのurl(file)分のFeedItemがかえってくること"


def test_Rss_make_articles():
    feed_list = []
