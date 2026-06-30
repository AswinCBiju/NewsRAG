This is a RAG project featuring a gemini agent which pulls news from various sources, cites them and generates simplified news report


# Requirements

1. Google gemini (or any preferable agent) API key
2. NewsAPI key
3. PostgreSQL

For functions follow these steps...
# NewsRAG

An AI-powered Retrieval-Augmented Generation (RAG) news assistant built using:

- React + Vite frontend
- FastAPI backend
- Google Gemini API
- NewsAPI
- PostgreSQL
- FAISS Vector Database
- Sentence Transformers embeddings

## Features

- Search for the latest news on any topic.
- Retrieval-Augmented Generation using FAISS.
- Automatic news fetching from NewsAPI.
- Conversational memory using session history.
- Trending topics support.
- Cached news retrieval using PostgreSQL.

---

## Project Structure

```text
NewsRAG/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── retrieval.py
│   ├── vector_store.py
│   ├── news_collector.py
│   ├── database.py
│   └── ...
│
└── README.md
```

---

## Prerequisites

Install the following:

- Python 3.11+
- Node.js 18+
- PostgreSQL
- pgAdmin (recommended)

---

## Backend Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install fastapi uvicorn psycopg2 python-dotenv
pip install langchain langchain-google-genai
pip install sentence-transformers faiss-cpu
pip install requests numpy
```

---

### Create PostgreSQL database

Create a database named:

```text
newsrag
```

---

### Create articles table

Run the following SQL inside pgAdmin Query Tool:

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    url TEXT UNIQUE,
    published_at TIMESTAMP,
    content TEXT,
    embeddings FLOAT8[],
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Create `.env`

Create a `.env` file inside:

```text
backend/.env
```

Example:

```env
GOOGLE_API_KEY=your_gemini_api_key
NEWS_API_KEY=your_news_api_key
DB_PASSWORD=your_postgresql_password
```

---

## API Keys

### Gemini API

Generate a Gemini API key from:

https://aistudio.google.com/app/apikey

---

### NewsAPI

Generate a NewsAPI key from:

https://newsapi.org/

---

## Running Backend

Navigate to backend:

```bash
cd backend
```

Start FastAPI:

```bash
py -m uvicorn main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

---

## Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## CORS Configuration

Ensure `main.py` contains:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
```

---

## Technologies Used

### Frontend

- React
- Vite
- TailwindCSS
- Axios

### Backend

- FastAPI
- LangChain
- Gemini API

### Database

- PostgreSQL

### Vector Search

- FAISS
- Sentence Transformers

---

## Notes

- `.env` should never be committed.
- `node_modules/` should not be committed.
- PostgreSQL must be installed locally.
- API keys are required for the application to function.

---

## Future Improvements

- Source citations in frontend
- Better relevance filtering
- Streaming responses
- Authentication
- Multi-user sessions
- Docker support