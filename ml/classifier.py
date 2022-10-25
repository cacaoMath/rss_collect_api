from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

dataset = pd.DataFrame([
  {"word": "ジャネット・ジャクソンのMVでPCがクラッシュする脆弱性", "category": "Windows"},
  {"word": "デスクトップ版「Outlook」に新たな問題、起動してもすぐ閉じてしまう", "category": "Windows"},
  {"word": "Windowsパッチに問題、インストールに失敗し「0x800f0922」エラーが表示される", "category": "Windows"},
  {"word": "Microsoft: KB5015882, KB5015814 updates break Start menu in Windows 11", "category": "Windows"},
  {"word": "Internet Explorer/EdgeHTMLで「TLS 1.0」「TLS 1.1」がデフォルト無効化へ", "category": "Windows"},
  {"word": "夏のゲーミングPCは熱すぎる！「MSI Afterburner」でビデオカードを省電力・低発熱に", "category": "other"},
  {"word": "「LibreOffice 7.4 Community」が公開、スプレッドシートで16,384列まで扱えるように", "category": "other"},
  {"word": "「Google Meet」でノイズキャンセリング量を音声インジケーターに表示可能に", "category": "other"},
  {"word": "いまさら聞けないExcelの使い方講座【好評連載中！】", "category": "other"},
])

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
