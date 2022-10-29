from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

dataset = pd.read_csv("ml/test_data.csv")

# カテゴリを数値化
dataset["y"], _ = pd.factorize(dataset["category"])

count_vectorizer = CountVectorizer()
# csr_matrix(疎行列)が返る
feature_vectors = count_vectorizer.fit_transform(dataset["word"])

clf = MultinomialNB()
clf.fit(feature_vectors, dataset["y"])

pred_x1 = "今秋正式リリースの「Windows 10 バージョン 22H2」にISOイメージファイル"
pred_x2 = "いまさら聞けないExcelの使い方講座【好評連載中！】"

result = clf.predict(count_vectorizer.transform([pred_x1]))
print("Windows" if result == 0 else "other")

result = clf.predict(count_vectorizer.transform([pred_x2]))
print("Windows" if result == 0 else "other")
