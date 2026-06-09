import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("dataset/classifier_dataset.csv")

X = df["question"]
y = df["topic"]

tfidf = TfidfVectorizer()

X_vec = tfidf.fit_transform(X)

model = LogisticRegression()

model.fit(X_vec, y)

joblib.dump(model, "models/topic_classifier.pkl")
joblib.dump(tfidf, "models/tfidf.pkl")

print("Model Saved")