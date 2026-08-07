# Sentinel AI 🛡️

[![CI Pipeline](https://github.com/sritamcodes/Sentinel-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/sritamcodes/Sentinel-AI/actions)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31011/)
[![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/vectorstore-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![Groq API](https://img.shields.io/badge/LLM-Groq%20(Llama%203.3%2070B)-violet.svg)](https://groq.com/)

An intelligent agentic system for automated document compliance, policy verification, and structured risk analysis using Retrieval-Augmented Generation (RAG).

---

## 🚀 Key Features

- **Document Analysis Engine:** Ingests and processes complex policy and compliance documents.
- **RAG Architecture:** Leverages ChromaDB for vector similarity search paired with local HuggingFace embeddings (`BAAI/bge-small-en-v1.5`).
- **Groq LLM Acceleration:** High-speed inference using `llama-3.3-70b-versatile`.
- **Modular Agent Skills:** Extensible skill architecture designed for rule enforcement and audit reporting.
- **Automated CI/CD:** Fully verified via GitHub Actions and Pytest test suites.

---

## 📐 Architecture Overview
```
+---------------------------------+
|        Streamlit Interface      |
|             (app.py)            |
+----------------+----------------+
                 |
                 v
+---------------------------------+
|      Sentinel Core Engine       |
|             (core/)             |
+----------------+----------------+
                 |
        +--------+--------+
        |                 |
        v                 v
+---------------+ +---------------+
|   ChromaDB    | | Custom Skills |
|  (chroma_db/) | |   (skills/)   |
+---------------+ +---------------+
```
Detailed architectural specifications, data flows, and design trade-offs are documented in [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 🛠️ Tech Stack

- **Framework & UI:** Streamlit, Python 3.10
- **Orchestration:** LangChain / LangChain-Groq
- **LLM Provider:** Groq Cloud API (`llama-3.3-70b-versatile`)
- **Embeddings:** HuggingFace `sentence-transformers` (`BAAI/bge-small-en-v1.5`)
- **Vector Database:** ChromaDB (Local persistence)
- **Testing & CI:** Pytest, GitHub Actions

---

## 📥 Installation & Setup

### Prerequisites

- Python 3.10 installed.
- A valid **Groq API Key** ([Get your key here](https://console.groq.com/keys)).

### 1. Clone the Repository

git clone [https://github.com/sritamcodes/Sentinel-AI.git](https://github.com/sritamcodes/Sentinel-AI.git)
cd Sentinel-AI

### 2. Create and Activate Virtual Environment

Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

### 3. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

### 4. Configure Environment Variables

Copy .env.example to .env and add your Groq API key:

cp .env.example .env

Inside .env:
GROQ_API_KEY=your_groq_api_key_here

---

## 🏃 Running the Application

Launch the Streamlit web interface:

streamlit run app.py

The application will be accessible at http://localhost:8501.

---

## 🧪 Testing

Run the test suite locally using pytest:

pytest

---

## 📑 Required Documentation

- ARCHITECTURE.md: High-level design, component diagrams, and tech stack details.
- agents.md: Behavioral guidelines and operational rules for Sentinel AI.
- agents_and_skills.md: Registry of implemented agents and custom skills.

---

## 🛡️ License

This project is licensed under the MIT License.
## 🏃 Running the Application

Launch the Streamlit web interface:

bash
streamlit run app.py

The application will be accessible at \`http://localhost:8501\`.

