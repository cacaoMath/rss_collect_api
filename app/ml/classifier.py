from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import pickle
from os.path import isfile

from app.util.ml_utils import make_van_list


class Classifier:
    def __init__(self) -> None:
        self.model_path = "classifier.pickle"
        self.classifier = Pipeline(steps=[
            # 文字の分析はml_utilの処理に任せるのでanalyzerを指定, 英単語は大小そのまま
            ("vec", CountVectorizer(lowercase=False, analyzer=lambda x:x)),
            ("tfidf", TfidfTransformer()),
            ("Classifier", MultinomialNB())
        ])

    def train(self, train_x, train_y) -> None:
        if isfile(self.model_path):
            self.__load_classifier
            vec = self.classifier["vec"].fit_transform(train_x, train_y)
            tfidf = self.classifier["tfidf"].fit(vec)
            self.classifier["Classifier"].partial_fit(tfidf)
        else:
            self.classifier.fit(train_x, train_y)
        self.__save_classifier

    def predict(self, pred_x: list[str]) -> list:
        result = self.classifier.predict(map(make_van_list, pred_x))
        self.__save_classifier
        return result

    def save_classifier(self) -> None:
        with open(self.model_path, mode="wb") as f:
            pickle.dump(self.classifier["Classifier"], f)
        print("aaaa")

    __save_classifier = save_classifier

    def load_classifier(self) -> None:
        with open(self.model_path, mode="rb") as f:
            self.classifier["Classifier"] = pickle.load(f)

    __load_classifier = load_classifier
