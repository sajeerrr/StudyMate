from sqlalchemy import Column,Integer,String,Float
from db.database import Base


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id =Column(Integer)
    topic = Column(String)
    difficulty = Column(String)
    score = Column(Integer)
    total = Column(Integer)
    percentage = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question = Column(String)
    answer = Column(String)