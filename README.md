# 🛡️ Sentinel AI — Compliance & Document Intelligence Workspace

Sentinel AI is a modern, privacy-focused Document Intelligence & Compliance Engine built with a custom **Claymorphic UI**. Powered by Retrieval-Augmented Generation (RAG), local vector embeddings via ChromaDB, and LangChain, Sentinel AI enables teams to ingest enterprise PDFs, audit risk factors, map structural citations, and perform Q&A without leaking sensitive data to external API dependencies.

---

## ✨ Features

* **🎨 Soft Claymorphic Interface:** Handcrafted, accessible UI built with customized Streamlit components, tactile 3D cards, and clean SVG vector icons.
* **🔒 Privacy-First RAG Pipeline:** Leverages local `sentence-transformers/all-MiniLM-L6-v2` embeddings via Hugging Face—no external API key required by default.
* **📄 Document Ingestion & Chunking:** Multi-page PDF parsing via `pypdf` with strict data cleaning and token-safe chunking to eliminate vectorization errors.
* **🎯 Citation Mapping & Risk Auditing:** Automatically maps source chunks back to exact document references for transparent compliance verification.
* **💬 Dynamic Segmented Workspace:** Clean, pill-shaped tab navigation separating **Document Q&A** and **Risk Audit** views.
* **🔑 Optional HF Token Integration:** Expand functionality seamlessly to gated models or inference endpoints through an in-app advanced settings toggle.

---

## 🛠️ Tech Stack

* **Frontend Framework:** [Streamlit](https://streamlit.io/) with custom CSS overrides & HTML5 SVGs
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **LLM & RAG Orchestration:** [LangChain](https://www.langchain.com/) / [LangChain-HuggingFace](https://python.langchain.com/)
* **Document Parser:** [PyPDF](https://pypdf.readthedocs.io/)
* **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (Local execution)

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Git

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

