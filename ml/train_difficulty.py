import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("dataset/difficulty_dataset.csv")

X = df["question"]
y = df["difficulty"]

tfidf = TfidfVectorizer()

X_vec = tfidf.fit_transform(X)

model = LogisticRegression(max_iter=1000)

model.fit(X_vec, y)

joblib.dump(model, "models/difficulty_model.pkl")
joblib.dump(tfidf, "models/difficulty_tfidf.pkl")

print("Model Saved")