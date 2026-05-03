"""
api/app.py
----------
FastAPI application entry point.

Run with:
    uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

Interactive docs available at:
    http://localhost:8000/docs    (Swagger UI)
    http://localhost:8000/redoc  (ReDoc)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import summarizer, timetable, email, crew

app = FastAPI(
    title="Multi-Agent Weekly Manager API",
    description=(
        "A multi-agent AI system for weekly productivity management. "
        "Provides PDF summarisation, weekly timetable generation, and Gmail draft creation "
        "via both CrewAI and LangChain implementations."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(summarizer.router, prefix="/summarize", tags=["Summarizer"])
app.include_router(timetable.router, prefix="/timetable", tags=["Timetable"])
app.include_router(email.router, prefix="/email", tags=["Email Drafter"])
app.include_router(crew.router, prefix="/crew", tags=["Full Crew"])


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Returns a simple health check response."""
    return {"status": "ok", "service": "Multi-Agent Weekly Manager"}
