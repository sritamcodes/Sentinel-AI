# Agents and Custom Skills (agents_and_skills.md)

## 1. System Agents

### Agent: Sentinel Core Orchestrator
- **Directory:** `core/`
- **Primary Function:** Receives user document input, chunks text, generates embeddings, interfaces with ChromaDB, and coordinates evaluation pipelines.
- **Tools Used:** LangChain / Groq API, Vector Retriever, Document Parsers.

---

## 2. Custom Skills Registry

### Skill: Document Compliance Processor
- **Directory / Module:** `skills/` (e.g., `skills/compliance_skill.py`)
- **Trigger Condition:** Activated when a user submits a document for verification, policy checking, or structural audit.
- **Capabilities:**
  - Extracts text content from incoming files.
  - Generates document embeddings stored in `chroma_db/`.
  - Executes rule-based and semantic compliance scans.
- **Input Schema:** Standardized file object or plain text string.
- **Output Schema:** Analysis summary with pass/fail markers and actionable recommendations.

---

## 3. Testing & Validation
All custom skills listed in `skills/` must be accompanied by unit tests inside the `tests/` directory (e.g., `tests/test_document_processor.py`).