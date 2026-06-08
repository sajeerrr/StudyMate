import joblib

model = joblib.load(
    "models/difficulty_model.pkl"
)

tfidf = joblib.load(
    "models/difficulty_tfidf.pkl"
)

def predict_difficulty(question):
    vec = tfidf.transform([question])
    prediction = model.predict(vec)

    return prediction[0]