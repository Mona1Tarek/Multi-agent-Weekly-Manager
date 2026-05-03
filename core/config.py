"""
core/config.py
--------------
Centralised configuration: loads environment variables and initialises
the shared LLM instance used by all agents.
"""

import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
AGENTOPS_API_KEY: str = os.getenv("AGENTOPS_API_KEY", "")
LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")

OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
INPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "input")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(INPUT_DIR, exist_ok=True)

# Shared CrewAI LLM instance (llama-3.1-8b-instant via Groq)
basic_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.7,
    api_key=GROQ_API_KEY,
)

# Shared LangChain ChatGroq instance (lazy import to avoid circular deps)
def get_langchain_llm():
    from langchain_groq import ChatGroq
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.7,
        api_key=GROQ_API_KEY,
    )
