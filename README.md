# StudyMate – AI-Powered Learning Assistant

**Demo Link:**  [Watch the StudyMate Demo on Youtube](https://youtu.be/4w-RXfVZr00)

## Overview

StudyMate is an AI-powered learning platform that helps students learn from their study materials more effectively. Users can upload PDF documents, interact with an AI tutor, generate quizzes, and track learning performance through analytics.

The system combines Retrieval-Augmented Generation (RAG), vector search, and Large Language Models to provide context-aware educational assistance.

---

## Features

### AI Chat with Study Material

* Upload PDF notes and textbooks
* Ask questions about uploaded documents
* Context-aware answers using RAG

### Quiz Generation

* Generate quizzes from study materials
* Multiple difficulty levels
* Automatic scoring

### Learning Analytics

* Track quiz performance
* Topic-wise score analysis
* Difficulty-wise performance insights
* Personalized recommendations

### Authentication

* User registration and login
* JWT-based authentication
* Protected API routes

### Database Support

* PostgreSQL for persistent storage
* User management
* Quiz history tracking

---

## Architecture

```text
Frontend (Streamlit)
        │
        ▼
FastAPI Backend
        │
        ▼
RAG Pipeline
        │
        ▼
ChromaDB Vector Store
        │
        ▼
Groq LLM
```

### System Flow

1. User uploads PDF
2. PDF is processed and split into chunks
3. Chunks are converted into embeddings
4. Embeddings are stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved
7. Context is sent to Groq LLM
8. AI generates an answer

---

## Tech Stack

### Backend

* FastAPI
* Python
* SQLAlchemy
* JWT Authentication

### Database

* PostgreSQL

### AI & RAG

* LangChain
* ChromaDB
* Sentence Transformers
* HuggingFace Embeddings
* Groq LLM

### Frontend

* Streamlit

### DevOps

* Docker
* Docker Compose
* GitHub Actions

---

## Project Structure

```text
StudyMate/
│
├── app/
├── db/
├── rag/
├── frontend/
├── tests/
│
├── main.py
├── auth.py
├── models.py
├── schemas.py
├── analytics.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/sajeerrr/StudyMate.git
cd StudyMate
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
DATABASE_URL=your_database_url
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

### Run FastAPI

```bash
uvicorn main:app --reload
```

### Run Streamlit

```bash
streamlit run frontend/app.py
```

---

## Docker Deployment

Build image:

```bash
docker build -t studymate .
```

Run container:

```bash
docker run -p 8000:8000 studymate
```

Using Docker Compose:

```bash
docker compose up --build
```

---

## API Documentation

After starting the backend:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

## Testing

Run tests:

```bash
pytest
```

GitHub Actions automatically runs tests on every push.

---

## Screenshots

### Home Page

Add screenshot here.

### AI Chat

Add screenshot here.

### Quiz Generation

Add screenshot here.

### Analytics Dashboard

Add screenshot here.

---

## Future Improvements

* Voice-based learning assistant
* Flashcard generation
* Multi-document retrieval
* Study schedule planner
* OCR support for scanned PDFs
* Collaborative study groups
* Advanced analytics dashboard
* Mobile application

---
