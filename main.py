from fastapi import FastAPI,UploadFile,File,Depends

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embedder import get_embedding_model
from rag.vector_store import create_vector_store,load_vector_store
from rag.chatbot import ask_rag
from rag.quiz_generator import generate_quiz,evaluate_quiz

from schemas import ChatRequest,ChatResponse,QuizRequest,QuizSubmission,QuizStore
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml import difficulty,classifier

from db.database import engine,Base,SessionLocal
from db.models import QuizResult
from sqlalchemy.orm import Session
from analytics import get_analytics,analyze_topics,recommend_topics


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title = "StudyMate",
    version = "1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message":"StudyMate Running"
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    filepath = f"data/{file.filename}"

    with open(filepath,"wb") as f:
        f.write(await file.read())

    docs = load_pdf(filepath)

    chunks = split_documents(docs)

    embeddings = get_embedding_model()

    create_vector_store(chunks,embeddings)

    return {
        "message":"PDF Processed Successfully"
    }

@app.post("/chat",response_model=ChatResponse)
def chat(request: ChatRequest):
    embeddings = get_embedding_model()

    db = load_vector_store(embeddings)

    answer = ask_rag(
        request.question,
        db
    )

    return ChatResponse(answer=answer)



@app.post("/predict-difficulty")
def predict(request: ChatRequest):
    level = difficulty.predict_difficulty(
        request.question
    )

    return {
        "difficulty": level
    }


@app.post("/classify-topic")
def classify(request: ChatRequest):
    topic = classifier.predict_topic(
        request.question
    )

    return {
        "Topic": topic
    }


@app.post("/quiz")
def create_quiz(request: QuizRequest):
    quiz = generate_quiz(
        request.topic,
        request.difficulty,
        request.num_questions
    )

    return quiz

# @app.post("/submit")
# def submit_quiz(request: QuizSubmission):
#     result = evaluate_quiz(
#         request.questions,
#         request.answers
#     )

#     return result

@app.post("/submit-quiz")
def submit_quiz(
    submission: QuizStore,
    db: Session = Depends(get_db)
):

    percentage = (submission.score/submission.total)*100

    result = QuizResult(
        topic = submission.topic,
        difficulty = submission.difficulty,
        score = submission.score,
        total = submission.total,
        percentage = percentage
    )

    db.add(result)
    db.commit()

    return {
        "message": "Result Saved"
    }


@app.post("/analytics")
def analytics(db: Session = Depends(get_db)):
    data = get_analytics(db)
    strong, weak = analyze_topics(data)

    return {
        "strong_topics": strong,
        "weak_topics": weak
    }

@app.post("/recomendations")
def recommendations(db: Session = Depends(get_db)):
    data = get_analytics(db)
    strong, weak = analyze_topics(data)

    recs = recommend_topics(weak)

    return {
        "recommendations": recs
    }

@app.get("/dashboard")
def dashboard(db:Session = Depends(get_db)):
    results = db.query(QuizResult.all())

    total_quizzes = len(results)

    if total_quizzes > 0:
        average_score = round(
            sum(r.percentage for r in results)/total_quizzes,2
        )
    else:
        average_score = 0
    
    strong, weak =analyze_topics(db)
    recommendations = recommend_topics(weak)

    return {
        "total_quizzes": total_quizzes,
        "average_score": average_score,
        "strong_topics": strong,
        "weak_topics": weak,
        "recommendations": recommendations
    }