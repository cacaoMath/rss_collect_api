#　my rss api
## 概要
- RSS の記事(内容)をjsonとして返すAPIを目指す
- 返すRSSの特徴
    - ジャンル分けをして、ジャンルに合ったものを返す(とりあえずwindows news用)
    - さまざまなRSSから、上記のジャンルに合ったものを抽出する
- APIとして実装したい機能
  - RSS feedのURLを追加・削除する
  - その日のさまざまなRSS記事の内容をジャンルで厳選してJsonで返す
  - 学習データの追加および学習・削除
- RSSを厳選する方法
  - ナイーブベイズを使って簡単な機械学習で行う(マシンスペックが許せば将来的には深層学習も使うかもしれない)

## ジャンル推定
### ナイーブベイズ
- 簡単に実装するためsklearnにあるものを使う
  - 精度を高めるために、BOWや正規化などの前処理は行う
- 参考
  - Skleanで推定
    - http://neuro-educator.com/ml7/
    - https://qiita.com/asakbiz/items/73c552babd3bbca987f9
    - https://qiita.com/fujin/items/39d450b910bf2be866b5
  - 前処理
    - https://note.com/shimakaze_soft/n/nf02b0f8ab0f6
    - https://qiita.com/kiyuka/items/3de09e313a75248ca029

  - FASTAPI CRUD
    - https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#__tabbed_1_3
  - Sqalchemy
    - https://qiita.com/petitviolet/items/e03c67794c4e335b6706

### 形態素分析
  - 比較的新言語に対応していると思われる以下の辞書を使用する。Mecabなどは手順通りに入れる
    - https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md


## test
- pytestを使用
- 参考
  - dbのfixture
    - https://note.com/navitime_tech/n/n5286eecf5a7c

## API
### `feeds`
- `/feeds/` : GET
  - 登録しているRSS feed URLの一覧表示
- `/feeds/{feed_id}` : GET
  - {feed_id}のRSS feed URLの表示
- `/feeds/{feed_id}` : UPDATE
  - {feed_id}のRSS feed URLの更新
- `/feeds/{feed_id}` : DELETE
  - {feed_id}のRSS feed URLの削除
- `/feeds/` : POST
  - RSS feed URLの登録

### `learning-data`
- `/learning-data/` : GET
  - 学習データの一覧表示
- `/learning-data/{data_id}` : GET
  - {data_id}の学習データを表示
- `/learning-data/{data_id}` : UPDATE
  - {data_id}の学習データを更新
- `/learning-data/{data_id}` : DLETE
  - {data_id}の学習データを削除
- `/learning-data/` : POST
  - 学習データの追加

### `classifier`
- `/classifier` : GET
  - モデル更新日出力
- `/classifier/predict` : POST
  - テキストのジャンルを推定
### `rss`
- `/rss/` : GET
  - 分類器を使用して、ジャンル分けされた記事のタイトル、日付、URLなどをJSONで返す

## Model
### feeds
- url: str
  - valid
    - length: 255
    - null: false
- description : str | None
  - valid
    - length: 255
- is_active
  - valid
    - default: True
### learning-data
- word: str
  - valid
    - length: 255
    - null: false
- category: str
  - valid
    - length: 10
    - null: false
    - 使用できる文字: a-z,A-Z,数字,_のみとする

## デプロイ方法
- デプロイするサーバにmecabの辞書`mecab-ipadic-NEologd`をインストールする
  - 方法は公式に従う: https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
  - `$ echo `mecab-config --dicdir`"/mecab-ipadic-neologd"`で辞書が確認できればOK
- deploy.shを叩く
  - deploy.shで必要なDockerfileのビルドや辞書のコピーなどが行われる。
- deploy完了、localhost:8000で接続できるか確認する