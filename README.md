<div align="center">

# StudyMate
### AI-Powered Learning Assistant

**Transform your study materials into an interactive learning experience**

[Watch Demo in Youtube](https://youtu.be/4w-RXfVZr00)

---

</div>

## Overview

**StudyMate** is a full-stack AI learning platform that turns static PDF study materials into an interactive, intelligent tutor. Upload your notes or textbooks, and StudyMate lets you chat with the content, auto-generate quizzes, and track your learning progress — all powered by a RAG pipeline backed by Groq LLM.

> Built with FastAPI · LangChain · ChromaDB · Streamlit · PostgreSQL · Docker

---

## Features

| Feature | Description |
|---|---|
| **AI Chat** | Ask questions about your uploaded PDFs — context-aware answers via RAG |
| **Quiz Generation** | Auto-generate quizzes at multiple difficulty levels with automatic scoring |
| **Learning Analytics** | Topic-wise and difficulty-wise performance tracking with personalized recommendations |
| **Authentication** | JWT-based user registration, login, and protected API routes |
| **Persistent Storage** | PostgreSQL-backed user management and full quiz history |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (Streamlit)                │
└────────────────────┬────────────────────────────┘
                     │  HTTP / REST
┌────────────────────▼────────────────────────────┐
│             FastAPI Backend                      │
│   auth.py · analytics.py · models.py            │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│               RAG Pipeline                       │
│  PDF → Chunks → Embeddings → ChromaDB           │
└────────┬───────────────────────┬────────────────┘
         │                       │
┌────────▼────────┐   ┌──────────▼──────────────┐
│  ChromaDB       │   │  Groq LLM               │
│  Vector Store   │   │  (Context + Answer)     │
└─────────────────┘   └─────────────────────────┘
```

### Request Flow

```
User uploads PDF
      │
      ▼
PDF split into chunks
      │
      ▼
Sentence Transformers generate embeddings
      │
      ▼
Embeddings stored in ChromaDB
      │
      ▼
User asks a question
      │
      ▼
Top-k relevant chunks retrieved
      │
      ▼
Context + question sent to Groq LLM
      │
      ▼
AI answer returned to user
```

---

## Tech Stack

### Backend & API

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| ORM | SQLAlchemy |
| Authentication | JWT (PyJWT) |
| Language | Python 3.10+ |

### AI & RAG

| Component | Technology |
|---|---|
| Orchestration | LangChain |
| Embeddings | Sentence Transformers (HuggingFace) |
| Vector Store | ChromaDB |
| LLM | Groq (LLaMA 3) |

### Frontend & Database

| Component | Technology |
|---|---|
| UI | Streamlit |
| Primary Database | PostgreSQL |

### DevOps

| Component | Technology |
|---|---|
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Testing | Pytest |

---

## Project Structure

```
StudyMate/
│
├── app/                    # Core application modules
├── db/                     # Database config and migrations
├── rag/                    # RAG pipeline (chunking, embeddings, retrieval)
├── frontend/               # Streamlit UI
│   └── app.py
├── tests/                  # Pytest test suite
│
├── main.py                 # FastAPI entry point
├── auth.py                 # JWT authentication
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── analytics.py            # Learning analytics logic
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Docker (optional)
- Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/sajeerrr/StudyMate.git
cd StudyMate
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/studymate
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret_key
```

### 5. Run the Application

**Start FastAPI backend:**
```bash
uvicorn main:app --reload
```

**Start Streamlit frontend** (in a separate terminal):
```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501` in your browser.

---

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t studymate .

# Run container
docker run -p 8000:8000 studymate
```

### Using Docker Compose (Recommended)

```bash
docker compose up --build
```

This starts FastAPI, Streamlit, and PostgreSQL together in one command.

---

## API Reference

After starting the backend, interactive API docs are available at:

| Interface | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

### Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive JWT token |
| `POST` | `/upload` | Upload a PDF document |
| `POST` | `/chat` | Ask a question about uploaded material |
| `POST` | `/quiz/generate` | Generate a quiz from study material |
| `GET` | `/analytics/me` | Fetch personal learning analytics |

---

## Testing

```bash
pytest
```

Tests run automatically on every push via **GitHub Actions CI**.

---

## Screenshots

| Home Page | AI Chat |
|---|---|
| ![Home](screenshots/home.png) | ![Chat](screenshots/chat.png) |

| Quiz Generation | Analytics Dashboard |
|---|---|
| ![Quiz](screenshots/quiz.png) | ![Analytics](screenshots/analytics.png) |

---
