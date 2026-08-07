# Sentinel AI - System Architecture

## Overview
Sentinel AI is an automated agentic system designed to ingest, process, and analyze compliance documents using vector embeddings and LLM orchestration.

## Tech Stack
- **Framework:** Python 3.10 / Streamlit
- **LLM Orchestration:** LangChain / Groq API
- **Vector Database:** ChromaDB
- **Testing:** Pytest & GitHub Actions CI

## Data Flow & System Components
1. **Ingestion & Processing (`core/`):** Reads input documents, chunks text, and generates embeddings.
2. **Storage (`chroma_db/`):** Persists document vectors for fast similarity retrieval.
3. **Agent & Skills (`skills/`):** Modular tools invoked by the core engine to evaluate rules and run checks.
4. **Interface (`app.py`):** Streamlit UI for user interactions and query processing.

## Security & Guardrails
- Local execution of vector store.
- Environment credentials managed via `.env`.