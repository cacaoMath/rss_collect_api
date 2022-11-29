# RSS colelct API
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

## 内容一覧
- [システム構成](#システム構成)
- [デプロイ方法](#デプロイ方法)
- [API 概要](#api) (未実装含む)
  - [実装されているAPI詳細](https://api.cacaomath.com/redoc)
- [Model](#model)
- [Schema](#schema型データ)
- [参考](#参考)

## システム構成例
![rss_collect_api drawio](https://user-images.githubusercontent.com/53263220/204059826-0513a4fe-d668-45c3-b8dc-7f753f2c379e.svg)

- frp: https://github.com/fatedier/frp
  - ポート解放ができないローカルのサーバ公開のために使用
- DB: Prostgres


## デプロイ方法
- デプロイするサーバにmecabの辞書`mecab-ipadic-NEologd`をインストールする
  - 方法は公式に従う: https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
  - `$ echo `mecab-config --dicdir`"/mecab-ipadic-neologd"`で辞書が確認できればOK

- checkoutしてくる
```
$ git clone git@github.com:cacaoMath/rss_collect_api.git
$ git checkout ${デプロイするバージョンタグ名}
```
- .envファイルに必要な値を入力する
  - `.env.sample`を例にする
- deploy.shを叩く
  - deploy.shで必要なDockerfileのビルドや辞書のコピーなどが行われる。
- deploy完了、localhost:8000などで接続できるか確認する

## 開発環境構築
- pipenvでパッケージ管理しているためインストールしておく
- `pipenv install --dev`で開発に必要なパッケージ込みでインストール可能
- 内部処理に使用してる`mecab-ipadic-NEologd`は別で要インストール
  - 方法は公式に従う: https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
- DBはDockerで立ち上げられる
  - `cp docker-compose.yml.sample docker-compose.yml`の後にdocker-composeで立ち上げる
- `.env`にDB情報などの記入が必要なので`.env.sample`を参考に記入し作成する。

## API
- `/docs` or `/redoc`で詳細の確認が可能
- POST,UPDATE,DELETEの処理はBASIC認証が必要
  - `/rss`は例外とする
### `feeds`
- `/feeds` : GET
  - 登録しているRSS feed URLの一覧表示
- `/feeds/{feed_id}` : GET
  - {feed_id}のRSS feed URLの表示
- `/feeds/{feed_id}` : UPDATE
  - {feed_id}のRSS feed URLの更新
- `/feeds/{feed_id}` : DELETE
  - {feed_id}のRSS feed URLの削除
- `/feeds` : POST
  - RSS feed URLの登録

### `learning-data`
- `/learning-data` : GET
  - 学習データの一覧表示
- `/learning-data/{data_id}` : GET
  - {data_id}の学習データを表示
- `/learning-data/{data_id}` : UPDATE
  - {data_id}の学習データを更新
- `/learning-data/{data_id}` : DLETE
  - {data_id}の学習データを削除
- `/learning-data` : POST
  - 学習データの追加

### `categories`
- `/categories` : GET
  - 登録されているカテゴリ(ジャンル)の一覧表示

### `classifier`
- `/classifier` : GET　（学習モデルが保存できる場合に実装）
  - 機械学習モデル更新日出力
- `/classifier/predict` : POST
  - テキストのジャンルを推定

### `rss`
- `/rss` : POST
  - 分類器を使用して、POSTしたジャンルで集められた記事のタイトル、日付、URLなどをJSONで返す
  - RequesBody: JSON
    ```
    {"categories": ["string1", "string2", ...]}
    ```
    - "categories"にはGET `/categories`得られる値から、得たい記事のジャンルをlistで入れる。
#### `/rss`内部処理
![rss](https://user-images.githubusercontent.com/53263220/204524031-ae49e9d1-ee73-4bfa-b81d-b01fece926f4.svg)



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
- category_id: Categoryのデータに紐づくid
- category : Categoryとリレーション

### Category
- category: str
  - valid
    - length: 30
    - null: false
    - 使用できる文字: a-z,A-Z,0-9,-

## Schema(型データ)
- [docsのschemas](https://api.cacaomath.com/docs)を参照

## 参考
### ジャンル推定
#### ナイーブベイズ
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

#### 形態素分析
  - 比較的新言語に対応していると思われる以下の辞書を使用する。Mecabなどは手順通りに入れる
    - https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md

### rss_feed
- feedparserを使う
  - https://pythonhosted.org/feedparser/

### Test
- pytestを使用
- 参考
  - dbのfixture
    - https://note.com/navitime_tech/n/n5286eecf5a7c