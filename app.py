import streamlit as st
import time
from core.document_processor import process_uploaded_files, get_text_chunks
from core.vectorstore import build_vectorstore, get_retriever
from core.rag_engine import create_sentinel_rag_chain
from skills.compliance_skill import run_compliance_audit

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sentinel AI — Enterprise Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Premium CSS Design System ────────────────────────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════════════
       SENTINEL AI — Executive Design System
       Color: Indigo/Electric Blue on Enterprise Slate
       Typography: Plus Jakarta Sans + JetBrains Mono
       ═══════════════════════════════════════════════════════════════════════ */

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global Reset ──────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .main {
        background: linear-gradient(165deg, #0f1117 0%, #13151d 35%, #151821 70%, #111320 100%);
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 980px;
    }

    /* ── Scrollbar ─────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.5); }

    /* ── Sidebar ───────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f14 0%, #111319 50%, #0f1117 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.875rem;
    }

    /* ── Header Brand ──────────────────────────────────────────────────── */
    .sentinel-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 0.25rem 0 1rem 0;
    }

    .sentinel-logo {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1 0%, #818cf8 50%, #a5b4fc 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3), 0 0 40px rgba(99, 102, 241, 0.1);
        flex-shrink: 0;
    }

    .sentinel-header-text {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .sentinel-header-title {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }

    .sentinel-header-sub {
        font-size: 0.78rem;
        font-weight: 400;
        color: rgba(148, 163, 184, 0.7);
        letter-spacing: 0.04em;
    }

    /* ── Status Badge ──────────────────────────────────────────────────── */
    .sentinel-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 10.5px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        background: rgba(99, 102, 241, 0.08);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.18);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s ease-in-out infinite;
    }

    .status-dot.active {
        background-color: #10b981;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
    }

    .status-dot.standby {
        background-color: #f59e0b;
        box-shadow: 0 0 6px rgba(245, 158, 11, 0.4);
    }

    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.85); }
    }

    /* ── Hero Section ──────────────────────────────────────────────────── */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.1;
        margin-bottom: 0.25rem;
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 40%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1rem;
        font-weight: 400;
        color: rgba(148, 163, 184, 0.85);
        margin-bottom: 1.75rem;
        line-height: 1.55;
        max-width: 640px;
    }

    /* ── Cards & Containers ────────────────────────────────────────────── */
    .glass-card {
        padding: 2rem 1.75rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.08);
    }

    /* ── Empty State ───────────────────────────────────────────────────── */
    .empty-state-card {
        padding: 4rem 2.5rem;
        text-align: center;
        border: 1px dashed rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        margin-top: 1.5rem;
        background: radial-gradient(ellipse at center, rgba(99, 102, 241, 0.03) 0%, transparent 70%);
        position: relative;
        overflow: hidden;
    }

    .empty-state-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.04) 0%, transparent 50%);
        animation: ambient-rotate 20s linear infinite;
    }

    @keyframes ambient-rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 1.25rem;
        display: block;
        position: relative;
        z-index: 1;
        filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.2));
    }

    .empty-state-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
        color: #e2e8f0;
        position: relative;
        z-index: 1;
    }

    .empty-state-desc {
        font-size: 0.875rem;
        color: rgba(148, 163, 184, 0.75);
        max-width: 440px;
        margin: 0 auto;
        line-height: 1.65;
        position: relative;
        z-index: 1;
    }

    .empty-state-steps {
        margin-top: 1.75rem;
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }

    .step-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 500;
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        letter-spacing: 0.01em;
    }

    .step-num {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: #818cf8;
    }

    /* ── Sidebar Branding Card ─────────────────────────────────────────── */
    .sidebar-brand {
        padding: 1.25rem;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(99, 102, 241, 0.02) 100%);
        border: 1px solid rgba(99, 102, 241, 0.12);
        margin-bottom: 1.25rem;
    }

    .sidebar-brand-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 4px;
    }

    .sidebar-brand-tagline {
        font-size: 0.75rem;
        color: rgba(148, 163, 184, 0.6);
        font-weight: 400;
    }

    .sidebar-section-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(148, 163, 184, 0.45);
        margin: 1.25rem 0 0.6rem 0;
    }

    /* ── Model Info Card ───────────────────────────────────────────────── */
    .model-info {
        padding: 0.85rem 1rem;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 0.5rem;
    }

    .model-info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        font-size: 0.78rem;
    }

    .model-info-label {
        color: rgba(148, 163, 184, 0.55);
        font-weight: 500;
    }

    .model-info-value {
        color: #cbd5e1;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        background: rgba(99, 102, 241, 0.08);
        padding: 2px 8px;
        border-radius: 5px;
    }

    /* ── Button Styling ────────────────────────────────────────────────── */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.6rem 1.25rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.01em !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25), 0 0 0 1px rgba(99, 102, 241, 0.1) !important;
        color: #fff !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.35), 0 0 0 1px rgba(99, 102, 241, 0.2) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    /* ── Tab Styling ───────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.84rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        padding: 0.55rem 1.25rem;
        color: rgba(148, 163, 184, 0.7);
        transition: all 0.2s ease;
        border: none;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0;
        background: rgba(99, 102, 241, 0.06);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.12) !important;
        color: #a5b4fc !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ── Chat Messages ─────────────────────────────────────────────────── */
    [data-testid="stChatMessage"] {
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.04);
        background: rgba(255, 255, 255, 0.015);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: border-color 0.25s ease;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(99, 102, 241, 0.12);
    }

    /* ── Chat Input ────────────────────────────────────────────────────── */
    [data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* ── Expander (Source Citations) ────────────────────────────────────── */
    [data-testid="stExpander"] {
        border: 1px solid rgba(99, 102, 241, 0.12) !important;
        border-radius: 12px !important;
        background: rgba(99, 102, 241, 0.03) !important;
        margin-top: 0.5rem;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        font-size: 0.82rem;
        color: #a5b4fc;
        letter-spacing: 0.01em;
    }

    /* ── File Uploader ─────────────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] section {
        border: 1px dashed rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        background: rgba(99, 102, 241, 0.03) !important;
        padding: 1.25rem !important;
        transition: border-color 0.2s ease, background 0.2s ease;
    }

    [data-testid="stFileUploader"] section:hover {
        border-color: rgba(99, 102, 241, 0.35) !important;
        background: rgba(99, 102, 241, 0.05) !important;
    }

    /* ── Spinner ────────────────────────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: #818cf8 !important;
    }

    /* ── Success / Warning / Error Alerts ───────────────────────────────── */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        font-size: 0.84rem !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* ── Divider ───────────────────────────────────────────────────────── */
    [data-testid="stHorizontalBlock"] hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
    }

    /* ── Source Citation Card ───────────────────────────────────────────── */
    .source-card {
        padding: 0.75rem 1rem;
        border-radius: 10px;
        background: rgba(99, 102, 241, 0.04);
        border: 1px solid rgba(99, 102, 241, 0.1);
        margin-bottom: 0.65rem;
        transition: border-color 0.2s ease;
    }

    .source-card:hover {
        border-color: rgba(99, 102, 241, 0.25);
    }

    .source-card-header {
        font-size: 0.78rem;
        font-weight: 600;
        color: #818cf8;
        margin-bottom: 0.35rem;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .source-card-content {
        font-size: 0.8rem;
        color: rgba(148, 163, 184, 0.8);
        line-height: 1.5;
    }

    /* ── Compliance Report Styling ──────────────────────────────────────── */
    .compliance-report {
        padding: 1.5rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 0.75rem;
    }

    /* ── Stats Row ─────────────────────────────────────────────────────── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
    }

    .stat-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.06);
        border: 1px solid rgba(99, 102, 241, 0.12);
        color: #a5b4fc;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-chip .stat-icon {
        font-size: 0.85rem;
    }

    /* ── Hide Streamlit Defaults ────────────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

</style>
""", unsafe_allow_html=True)

# ─── Session State Initialization ─────────────────────────────────────────────
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_chunks" not in st.session_state:
    st.session_state.processed_chunks = None
if "file_count" not in st.session_state:
    st.session_state.file_count = 0
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand Card
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">🛡️ Sentinel AI</div>
        <div class="sidebar-brand-tagline">Enterprise Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Knowledge Ingestion Section
    st.markdown('<div class="sidebar-section-label">📁 Knowledge Ingestion</div>', unsafe_allow_html=True)
    st.caption("Upload policy manuals, audit notes, or compliance documentation.")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    if st.button("⚡ Process & Index Documents", type="primary", use_container_width=True):
        if uploaded_files:
            with st.spinner("Embedding documents into vector store..."):
                raw_docs = process_uploaded_files(uploaded_files)
                chunks = get_text_chunks(raw_docs)
                st.session_state.processed_chunks = chunks

                vectorstore = build_vectorstore(chunks)
                st.session_state.retriever = get_retriever(vectorstore)
                st.session_state.rag_chain = create_sentinel_rag_chain(st.session_state.retriever)

                st.session_state.file_count = len(uploaded_files)
                st.session_state.chunk_count = len(chunks)

                st.success(f"✅ Indexed {len(uploaded_files)} file(s) → {len(chunks)} chunks embedded.")
        else:
            st.warning("Upload at least one document to proceed.")

    # Index Stats
    if st.session_state.rag_chain:
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-chip"><span class="stat-icon">📄</span>{st.session_state.file_count} files</div>
            <div class="stat-chip"><span class="stat-icon">🧩</span>{st.session_state.chunk_count} chunks</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Model Details Card
    st.markdown('<div class="sidebar-section-label">🤖 Model Configuration</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="model-info">
        <div class="model-info-row">
            <span class="model-info-label">LLM</span>
            <span class="model-info-value">llama-3.3-70b</span>
        </div>
        <div class="model-info-row">
            <span class="model-info-label">Embeddings</span>
            <span class="model-info-value">bge-small-en-v1.5</span>
        </div>
        <div class="model-info-row">
            <span class="model-info-label">Vector DB</span>
            <span class="model-info-value">ChromaDB (MMR)</span>
        </div>
        <div class="model-info-row">
            <span class="model-info-label">Provider</span>
            <span class="model-info-value">Groq Cloud</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">ℹ️ About</div>', unsafe_allow_html=True)
    st.caption("Sentinel AI is a grounded enterprise Q&A and automated compliance risk engine. All responses are citation-backed from your uploaded documents.")


# ─── Main Canvas ──────────────────────────────────────────────────────────────

# Header with status badge
is_active = st.session_state.rag_chain is not None
status_class = "active" if is_active else "standby"
status_label = "Engine Active" if is_active else "Awaiting Documents"

st.markdown(f"""
<div class="sentinel-header">
    <div class="sentinel-logo">🛡️</div>
    <div class="sentinel-header-text">
        <div class="sentinel-header-title">Sentinel AI</div>
        <div class="sentinel-header-sub">Enterprise Intelligence & Compliance Engine</div>
    </div>
</div>
<div class="sentinel-badge">
    <span class="status-dot {status_class}"></span>
    {status_label}
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="hero-subtitle">Grounded document Q&A with citation verification and automated compliance risk auditing — powered by RAG.</p>', unsafe_allow_html=True)


# ─── Active State: Tabs ──────────────────────────────────────────────────────
if st.session_state.rag_chain:
    tab_chat, tab_audit = st.tabs(["💬 Intelligence Chat", "🛡️ Compliance Audit"])

    # ── Tab 1: Intelligence Chat ──────────────────────────────────────────
    with tab_chat:
        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # Render chat history
        for msg in st.session_state.chat_history:
            avatar = "🛡️" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                # Re-render sources for assistant messages
                if msg["role"] == "assistant" and "sources" in msg:
                    with st.expander("📍 Source Citations & Grounding Passages"):
                        for src in msg["sources"]:
                            st.markdown(f"""
                            <div class="source-card">
                                <div class="source-card-header">
                                    📄 Source [{src['idx']}]: {src['file']} &nbsp;|&nbsp; Page {src['page']}
                                </div>
                                <div class="source-card-content">{src['content'][:300]}{'...' if len(src['content']) > 300 else ''}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # Chat input
        if user_query := st.chat_input("Ask about your enterprise documents..."):
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_query)

            with st.chat_message("assistant", avatar="🛡️"):
                with st.spinner("Searching knowledge base..."):
                    response = st.session_state.rag_chain.invoke(user_query)
                    st.markdown(response)

                    # Source citations
                    sources = []
                    if st.session_state.retriever:
                        retrieved_docs = st.session_state.retriever.invoke(user_query)
                        with st.expander("📍 Source Citations & Grounding Passages"):
                            for idx, doc in enumerate(retrieved_docs, start=1):
                                src_file = doc.metadata.get("source", "Unknown")
                                src_page = doc.metadata.get("page", "N/A")
                                content = doc.page_content
                                sources.append({"idx": idx, "file": src_file, "page": src_page, "content": content})
                                st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-card-header">
                                        📄 Source [{idx}]: {src_file} &nbsp;|&nbsp; Page {src_page}
                                    </div>
                                    <div class="source-card-content">{content[:300]}{'...' if len(content) > 300 else ''}</div>
                                </div>
                                """, unsafe_allow_html=True)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "sources": sources
            })

    # ── Tab 2: Compliance Audit ───────────────────────────────────────────
    with tab_audit:
        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # Audit header card
        st.markdown("""
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
                <span style="font-size: 1.75rem;">🔍</span>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #e2e8f0;">Automated Compliance & Risk Audit</div>
                    <div style="font-size: 0.8rem; color: rgba(148,163,184,0.65); margin-top: 2px;">
                        Executes an autonomous AI evaluation across all indexed document chunks for risk and policy analysis.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        if st.button("🛡️ Run Compliance Audit", type="primary", use_container_width=True, key="audit_btn"):
            with st.spinner("Evaluating compliance guidelines and risk vectors..."):
                report = run_compliance_audit(st.session_state.processed_chunks)
                st.markdown(f"""
                <div class="compliance-report">
                    {report}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(report)

# ─── Inactive State: Empty Hero ──────────────────────────────────────────────
else:
    st.markdown("""
    <div class="empty-state-card">
        <span class="empty-state-icon">🛡️</span>
        <div class="empty-state-title">Sentinel Workspace Inactive</div>
        <div class="empty-state-desc">
            Upload your enterprise PDFs, Word documents, or policy files to activate the intelligence engine. All queries will be grounded against your documents with full citation tracing.
        </div>
        <div class="empty-state-steps">
            <div class="step-pill">
                <div class="step-num">1</div>
                Upload documents
            </div>
            <div class="step-pill">
                <div class="step-num">2</div>
                Process & Index
            </div>
            <div class="step-pill">
                <div class="step-num">3</div>
                Query & Audit
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)