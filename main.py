from fastapi import FastAPI,UploadFile,File,Depends,HTTPException

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
import os
import uuid


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
    # filepath = f"data/{file.filename}"
    unique_id = str(uuid.uuid4())
    unique_filename = (f"{unique_id}_{file.filename}")
    filepath = f"data/{unique_filename}"

    with open(filepath,"wb") as f:
        f.write(await file.read())

    docs = load_pdf(filepath)
    chunks = split_documents(docs)

    for chunk in chunks:
        if chunk.metadata is None:
            chunk.metadata = {}
        chunk.metadata["source"] = unique_filename
        chunk.metadata["original_name"] = file.filename

    embeddings = get_embedding_model()
    create_vector_store(chunks,embeddings)

    return {
        "message":"PDF Processed Successfully",
        "file_id": unique_filename
    }


@app.delete("/pdf/{file_id}")
def delete_pdf(file_id: str):
    filepath = f"data/{file_id}"

    if not os.path.exists(filepath):
        return{
            "error": "File not found"
        }
    
    os.remove(filepath)

    embeddings = get_embedding_model()
    vectordb = load_vector_store(embeddings)

    vectordb._collection.delete(
        where={"source": file_id}
    )

    return {
        "message": "PDF is deleted"
    }


@app.get("/files")
def get_files():
    files = []

    for filename in os.listdir("data"):
        if filename.endswith(".pdf"):
            orginal_name = "_".join(filename.split("_")[1:])
            files.append({
                "name": orginal_name,
                "file_id": filename
            })
    return files


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
    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Topic is required."
        )

    uploaded_files = [
        filename
        for filename in os.listdir("data")
        if filename.endswith(".pdf")
    ]

    if not uploaded_files:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF before generating a quiz."
        )

    try:
        quiz = generate_quiz(
            request.topic,
            request.difficulty,
            request.num_questions
        )
    except ValueError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {e}"
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
    results = db.query(QuizResult).all()

    total_quizzes = len(results)

    if total_quizzes > 0:
        average_score = round(
            sum(r.percentage for r in results)/total_quizzes,2
        )
    else:
        average_score = 0

    topic_data = get_analytics(db)
    strong, weak = analyze_topics(topic_data)
    recommendations = recommend_topics(weak)

    topic_scores = [
        {
            "topic": row.topic,
            "score": round(row.percentage, 2)
        }
        for row in topic_data
    ]

    difficulty_scores = {}
    for result in results:
        difficulty_scores.setdefault(result.difficulty, []).append(result.percentage)

    difficulty_scores = [
        {
            "difficulty": level,
            "score": round(sum(scores) / len(scores), 2),
            "quizzes": len(scores)
        }
        for level, scores in difficulty_scores.items()
    ]

    quiz_history = [
        {
            "id": result.id,
            "topic": result.topic,
            "difficulty": result.difficulty,
            "score": result.score,
            "total": result.total,
            "percentage": round(result.percentage, 2)
        }
        for result in results
    ]

    return {
        "total_quizzes": total_quizzes,
        "average_score": average_score,
        "strong_topics": strong,
        "weak_topics": weak,
        "recommendations": recommendations,
        "topic_scores": topic_scores,
        "difficulty_scores": difficulty_scores,
        "quiz_history": quiz_history
    }
