from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_news_agent
from vector_store import initialize_index
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_index()
    yield

app = FastAPI(lifespan=lifespan)

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories per session
chat_sessions = {}

class QueryRequest(BaseModel):
    question: str
    session_id: str = "default"


@app.post("/ask")
async def ask(request: QueryRequest):
    history = chat_sessions.get(request.session_id, [])
    response, updated_history = run_news_agent(request.question, history)
    chat_sessions[request.session_id] = updated_history
    return {"response": response, "session_id": request.session_id}

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    chat_sessions.pop(session_id, None)
    return {"message": "Session cleared"}

@app.get("/health")
async def health():
    return {"status": "ok"}