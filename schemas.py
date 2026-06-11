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

#for user login
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str