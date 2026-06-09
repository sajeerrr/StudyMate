from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    num_questions: int = 5

class QuizSubmission(BaseModel):
    questions: list
    answers: list


class QuizStore(BaseModel):
    topic: str
    difficulty: str
    score: int
    total: int