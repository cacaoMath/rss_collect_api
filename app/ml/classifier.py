from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

from app.util.ml_utils import make_van_list


class Classifier:
    def __init__(self) -> None:
        self.classifier = Pipeline(steps=[
            # 文字の分析はml_utilの処理に任せるのでanalyzerを指定, 英単語は大小そのまま
            ("vec", CountVectorizer(lowercase=False, analyzer=lambda x:x)),
            ("tfidf", TfidfTransformer()),
            ("Classifier", MultinomialNB())
        ])

    def train(self, train_x, train_y) -> None:
        self.classifier.fit(train_x, train_y)

    def predict(self, pred_x: list[str]) -> list:
        return self.classifier.predict(map(make_van_list, pred_x))
