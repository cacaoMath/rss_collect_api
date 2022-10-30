import MeCab
import re

# wakati = MeCab.Tagger("-Osimple -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
wakati = MeCab.Tagger("-Osimple -d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")


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
