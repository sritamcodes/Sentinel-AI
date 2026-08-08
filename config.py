import os
from dotenv import load_dotenv

# ── Load .env for local development ──────────────────────────────────────────
load_dotenv()

def _get_secret(key: str) -> str | None:
    """
    Resolve a secret with priority:
      1. os.environ / .env  (local dev)
      2. st.secrets          (Streamlit Cloud)
    Returns None if neither has the key.
    """
    value = os.getenv(key)
    if value:
        return value
    # Try Streamlit secrets (only available when running inside Streamlit)
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        return None

GROQ_API_KEY = _get_secret("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set.\n"
        "• Local dev: add it to your .env file (GROQ_API_KEY=gsk_...)\n"
        "• Streamlit Cloud: go to App Settings → Secrets and add:\n"
        "    GROQ_API_KEY = \"gsk_...\""
    )

# Groq LLM Backend
GROQ_MODEL = "llama-3.3-70b-versatile"

# Local CPU Embeddings (Fast, zero-cost, no rate-limits)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Chroma Storage Settings
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "sentinel_knowledge_base"