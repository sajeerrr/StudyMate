from langchain_chroma import Chroma
from .embedder import get_embedding_model
from .vector_store import load_vector_store

from .llm import generate_answer
import json


embeddings = get_embedding_model()

db = load_vector_store(embeddings)

def get_context(topic):
    retriever = db.as_retriever(
        search_kwargs={"k": 5}
    )

    docs = retriever.invoke(topic)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context

def generate_quiz(topic, difficulty, num_questions):

    context = get_context(topic)

    prompt = f"""
    Using ONLY the context below.

    Generate {num_questions} multiple choice questions.

    Context: {context}

    Difficulty: {difficulty}

    Return ONLY valid JSON.

    Format:

    [
    {{
        "question":"...",
        "option":[
         "...",
         "...",
         "...",
         "..."
        ],
        "answer":"..."
    }}
    ]
    """

    response = generate_answer(prompt)

    quiz = json.loads(response)

    return quiz


def evaluate_quiz(questions,answers):
    score = 0

    for q,ans in zip(questions,answers):
        if ans == q["answer"]:
            score += 1
    
    total = len(questions)
    percentage = round((score/total)*100,2)

    return {
        "score": score,
        "total": total,
        "percentage": percentage
    }