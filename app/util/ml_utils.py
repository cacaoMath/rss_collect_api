import MeCab
import re
from dotenv import load_dotenv
import os

load_dotenv("./.env")
wakati = MeCab.Tagger(f'-Osimple -d {os.environ.get("MECAB_DIC_PATH")}')


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
