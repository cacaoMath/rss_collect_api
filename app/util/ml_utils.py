import MeCab
import re
import pandas as pd
from sqlalchemy.orm import Session

from app.config.env import MECAB_DIC_PATH

wakati = MeCab.Tagger(f'-Osimple -d {MECAB_DIC_PATH}')


def perse_simple(text: str) -> list[list[str]]:
    """日本語でもいい感じに形態素分析する。なお全品詞が返る

    Args:
        text (str): 形態素分析を行うテキスト

    Returns:
        list[list[str]]: text='私負けましたわ'だと次のようになる:
        [['私', '名詞-代名詞-一般'], ['負け', '動詞-自立'],
        ['まし', '助動詞'], ['た', '助動詞'], ['わ', '助詞-終助詞']]
    """
    simple_wakati = wakati.parse(text).split("\n")
    # 最後の2要素は"EOF",""でいらないので落とす
    simple_wakati = simple_wakati[:-2]
    return [sw.split("\t") for sw in simple_wakati]


def is_van(text: str) -> bool:
    """名詞,形容詞,動詞といったことばがあるかを判定

    Args:
        text (str): 任意のtext

    Returns:
        bool: _description_
    """
    return bool(re.compile(r'(名詞|形容詞|動詞)').search(text))


def make_van_list(text: str) -> list[str]:
    """与えられたテキストから名詞、形容詞、動詞のみを抽出する

    Args:
        text (str): 文章

    Returns:
        list[str]: 文章を中の名詞、形容詞、動詞のみをリストにして返す
    """
    simple_persed_list = perse_simple(text)
    return [spl[0] for spl in simple_persed_list if is_van(spl[1])]


def make_dataset_from_db(db: Session) -> pd.DataFrame:
    """機械学習に使うデータ取得・データ整形

    Args:
        db (Session): dbのセッション

    Returns:
        pd.DataFrame: データフレームにして返す
    """

    dataset = pd.read_sql_query(
        sql="""
            SELECT word, category_id, text
            FROM learning_data
            INNER JOIN categories
            ON learning_data.category_id = categories.id
            """,
        con=db.bind
    )
    # 形態素分析を行う
    dataset["word"] = dataset["word"].apply(make_van_list)
    return dataset
