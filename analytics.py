from sqlalchemy import func
from db.models import QuizResult

def get_analytics(db):
    results = db.query(
        QuizResult.topic,
        func.avg(QuizResult.percentage)
    ).group_by(QuizResult.topic).all()

    return results

def analyze_topics(data):
    strong=[]
    weak=[]
    for topic,score in data:
        if score >= 75:
            strong.append(topic)

        if score < 60:
            weak.append(topic)

    return strong, weak

def recommend_topics(weak_topics):
    recommendations = []

    for topic in weak_topics:
        recommendations.append(f"Practice more {topic}")

    return recommendations