from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

from util.ml_utils import make_van_list

dataset = pd.read_csv("ml/test_data.csv")

classifier = Pipeline(steps=[
        # 文字の分析はml_utilの処理に任せるのでanalyzerを指定, 英単語は大小そのまま
        ("vec", CountVectorizer(lowercase=False, analyzer=lambda x: x)),
        ("tfidf", TfidfTransformer()),
        ("Classifier", MultinomialNB())
    ])

# カテゴリを数値化
dataset["y"], _ = pd.factorize(dataset["category"])
dataset["word"] = dataset["word"].apply(make_van_list)

classifier.fit(dataset["word"], dataset["y"])

pred_x1 = "今秋正式リリースの「Windows 10 バージョン 22H2」にISOイメージファイル"
pred_x2 = "いまさら聞けないExcelの使い方講座【好評連載中！】"

print(classifier.predict([make_van_list(pred_x1), make_van_list(pred_x2)]))
