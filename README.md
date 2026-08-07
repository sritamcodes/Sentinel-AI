# 🛡️ Sentinel AI — Enterprise Intelligence & Compliance Engine

> **Sentinel AI** is a zero-hallucination, high-speed enterprise knowledge assistant that converts complex organizational documents into audit-ready answers with strict source citation traceability and automated regulatory compliance scoring.

---

## 🌟 Key Features

- **Grounded Zero-Hallucination RAG:** Strict system prompt guardrails ensure the model answers strictly using retrieved enterprise context, explicitly stating when data is absent rather than fabricating information.
- **Deterministic Source Citation:** Every response provides clickable/expandable verified grounding passages, mapping answers back to the exact source file and page index.
- **Automated Compliance Audit Skill:** Run multi-chunk document scans to automatically highlight operational risk vectors, missing policy controls, and regulatory non-compliance.
- **Executive Dark-Mode UI:** Built with Streamlit and styled using custom high-contrast CSS for clean readability and modern enterprise UX.

---

## 🏗️ System Architecture

                             ┌───────────────────────────┐
                             │   Uploaded Enterprise     │
                             │  Docs (PDF, DOCX, TXT)    │
                             └─────────────┬─────────────┘
                                           │
                                           ▼
                             ┌───────────────────────────┐
                             │   PyPDF / Document Loader │
                             └─────────────┬─────────────┘
                                           │
                                           ▼
                             ┌───────────────────────────┐
                             │  Recursive Character      │
                             │  Text Splitter (Chunks)   │
                             └─────────────┬─────────────┘
                                           │
                                           ▼
┌──────────────────────────┐     ┌───────────────────────────┐
│ User Query (Streamlit)   ├────►│  Chroma Vector Store      │
└────────────┬─────────────┘     └─────────────┬─────────────┘
│                                 │
│           Retrieved Context     │
└────────────────────────────────►│
▼
┌───────────────────────────┐
│   LangChain LCEL Pipeline │
└─────────────┬─────────────┘
│
▼
┌───────────────────────────┐
│   Groq LLM Engine         │
│   (llama-3.3-70b)         │
└─────────────┬─────────────┘
│
▼
┌───────────────────────────┐
│ Grounded Response &       │
│ Traceable Source Citations│
└───────────────────────────┘


---

## 🛠️ Tech Stack

- **Frontend & UI:** Streamlit (Custom High-Contrast Design System)
- **Orchestration & Chains:** LangChain (LCEL Expression Language)
- **Vector Database:** ChromaDB
- **LLM Engine:** Groq (`llama-3.3-70b-versatile`)
- **Document Parsing:** PyPDF, python-docx

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Groq API Key ([Get your API Key](https://console.groq.com/))
- Hugging Face Token (Optional, for higher model download rate limits)

---

### Installation & Local Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/sentinel-ai.git](https://github.com/your-username/sentinel-ai.git)
   cd sentinel-ai
Create and Activate Virtual Environment

Bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Install Dependencies

Bash
pip install -r requirements.txt
Environment Configuration
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=gsk_your_groq_api_key_here
HF_TOKEN=hf_your_huggingface_token_here
CHROMA_PERSIST_DIR=./chroma_db
Run the Application

Bash
streamlit run app.py
📂 Project Structure
Plaintext
sentinel-ai/
├── core/
│   ├── document_processor.py   # PDF/DOCX ingestion & chunking
│   ├── vectorstore.py          # ChromaDB persistent vector index
│   └── rag_engine.py           # LangChain LCEL RAG pipeline & system prompts
├── skills/
│   └── compliance_skill.py     # Autonomous risk audit skill
├── .env                        # Environment variables (git-ignored)
├── app.py                      # Streamlit frontend & UI/UX logic
├── config.py                   # Central application configurations
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
📜 License
Distributed under the MIT License. See LICENSE for more information.
