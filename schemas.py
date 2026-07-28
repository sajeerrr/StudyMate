from pydantic import BaseModel, EmailStr

# Chat

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

# Quiz

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

# User

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str