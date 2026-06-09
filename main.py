from fastapi import FastAPI,UploadFile,File

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embedder import get_embedding_model
from rag.vector_store import create_vector_store,load_vector_store
from rag.chatbot import ask_rag

from schemas import ChatRequest,ChatResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml import difficulty



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


class DifficulyRequest(BaseModel):
    question: str

@app.post("/predict-difficulty")
def predict(request: DifficulyRequest):
    level = difficulty.predict_difficulty(
        request.question
    )

    return {
        "difficulty": level
    }