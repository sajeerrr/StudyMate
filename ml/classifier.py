import joblib

model = joblib.load(
    "models/topic_classifier.pkl"
)

tfidf = joblib.load(
    "models/tfidf.pkl"
)

def predict_topic(question):
    vec = tfidf.transform([question])
    
    return model.predict(vec)[0]