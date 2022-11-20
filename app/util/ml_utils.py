import MeCab
import re
import pandas as pd
from sqlalchemy.orm import Session

from app.util.env import MECAB_DIC_PATH

wakati = MeCab.Tagger(f'-Osimple -d {MECAB_DIC_PATH}')


def perse_simple(text: str) -> list[list[str]]:
    simple_wakati = wakati.parse(text).split("\n")
    # 最後の2要素は"EOF",""でいらないので落とす
    simple_wakati = simple_wakati[:-2]
    return [sw.split("\t") for sw in simple_wakati]


def is_van(text: str) -> bool:
    return bool(re.compile(r'(名詞|形容詞|動詞)').search(text))


def make_van_list(text: str) -> list[str]:
    simple_persed_list = perse_simple(text)
    return [spl[0] for spl in simple_persed_list if is_van(spl[1])]


def make_dataset_from_db(db: Session) -> pd.DataFrame:
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
