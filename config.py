import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Please add it to your .env file (e.g., GROQ_API_KEY=your_key) and restart the app.")

# Groq LLM Backend
GROQ_MODEL = "llama-3.3-70b-versatile"

# Local CPU Embeddings (Fast, zero-cost, no rate-limits)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Chroma Storage Settings
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "sentinel_knowledge_base"