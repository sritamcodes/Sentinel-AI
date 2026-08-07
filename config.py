import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq LLM Backend
GROQ_MODEL = "llama-3.3-70b-versatile"

# Local CPU Embeddings (Fast, zero-cost, no rate-limits)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Chroma Storage Settings
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "sentinel_knowledge_base"