from langchain_chroma import Chroma
from .embedder import get_embedding_model
from .vector_store import load_vector_store

from .llm import generate_answer
import json


def parse_quiz_response(response):
    cleaned = response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Quiz response did not contain a JSON list.")

    quiz = json.loads(cleaned[start:end + 1])

    if not isinstance(quiz, list) or not quiz:
        raise ValueError("Quiz response was empty.")

    for index, question in enumerate(quiz, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question {index} was not an object.")

        if not question.get("question"):
            raise ValueError(f"Question {index} is missing question text.")

        options = question.get("options")
        answer = question.get("answer")

        if not isinstance(options, list) or len(options) < 2:
            raise ValueError(f"Question {index} is missing answer options.")

        if answer not in options:
            raise ValueError(f"Question {index} answer is not in options.")

    return quiz

def get_context(topic):
    embeddings = get_embedding_model()
    db = load_vector_store(embeddings)

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
        "options":[
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

    quiz = parse_quiz_response(response)

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
