import streamlit as st
import time
import base64
import os
import markdown as md_lib
from core.document_processor import process_uploaded_files, get_text_chunks
from core.vectorstore import build_vectorstore, get_retriever
from core.rag_engine import create_sentinel_rag_chain
from skills.compliance_skill import run_compliance_audit

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sentinel — Compliance Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SVG Icons (Lucide) ────────────────────────────────────────────────────────
ICONS = {
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield-check"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    "file": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "user": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "bot": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cpu"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-circle-2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg>',
    "layer": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-layers"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 12 12 17 22 12"/><polyline points="2 17 12 22 22 17"/></svg>',
    "book": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-book-open"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    "github": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>'
}

# ─── Playful Claymorphic + SaaS CSS Design System ─────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════════════
       SENTINEL AI — Hybrid Design (Asymmetrical SaaS + Playful Claymorphism)
       Colors: Cream, Soft Apricot, Teal-Mint, Sunny Yellow
       Typography: DM Sans + IBM Plex Mono
       ═══════════════════════════════════════════════════════════════════════ */

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700;9..40,800&family=IBM+Plex+Mono:wght@500;600&display=swap');

    :root {
        --bg-main: #F0EBE4;
        --bg-card: #F9F7F5;
        --text-dark: #2C2825;
        --text-muted: #6b635e;
        
        /* Playful Accents */
        --apricot: #E07A5F;
        --mint: #81B29A;
        --yellow: #F4D35E;
        
        /* Claymorphism Shadows */
        --clay-out: 12px 12px 24px rgba(220, 210, 200, 0.4), -12px -12px 24px #FFFFFF;
        --clay-in: inset 2px 2px 4px rgba(255, 255, 255, 0.8), inset -2px -2px 4px rgba(0,0,0,0.05);
        
        /* Softer Shadows for Sidebar */
        --clay-sidebar-out: 6px 6px 14px rgba(180, 165, 150, 0.35), -6px -6px 14px #FFFFFF;
        
        /* Bouncy Animation */
        --bounce: all 0.2s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    }

    /* ── Global Reset ──────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, sans-serif;
        color: var(--text-dark);
        -webkit-font-smoothing: antialiased;
        background-color: var(--bg-main) !important;
    }

    [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stHeader"] {
        background-color: var(--bg-main) !important;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 4rem;
        max-width: 1140px;
    }

    h1, h2, h3, h4, h5, h6, p, div, span {
        color: var(--text-dark);
    }

    p {
        color: var(--text-muted);
    }

    /* ── Scrollbar ─────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg-main); }
    ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }

    /* ── Sidebar Synchronization ───────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--bg-main) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 2px 0 10px rgba(0,0,0,0.03);
    }

    [data-testid="stSidebar"] * {
        color: var(--text-dark) !important;
    }

    .sidebar-card {
        background: var(--bg-card);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: var(--clay-sidebar-out);
        margin-bottom: 1.5rem;
        text-align: center;
        transition: var(--bounce);
    }

    /* ── Native Widget Clay Styling ────────────────────────────────────── */
    .stApp > header {
        background: transparent !important;
    }
    
    [data-testid="stTextInput"] input {
        border-radius: 20px !important;
        background-color: #E8E0D8 !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: inset 3px 3px 6px rgba(180, 165, 150, 0.3), inset -3px -3px 6px #FFFFFF !important;
        color: var(--text-dark) !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 500 !important;
    }
    
    /* Force readable text inside all input fields and chat boxes */
    [data-testid="stChatInput"] textarea,
    [data-testid="stTextInput"] input,
    div[data-baseweb="textarea"] textarea {
        color: #1A1817 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background-color: #E8E0D8 !important;
    }
    /* Style placeholder text so it remains readable */
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #7A7268 !important;
    }

    /* Target Streamlit file uploader button and drop area */
    [data-testid="stFileUploader"] section {
        background-color: #E8E0D8 !important;
        border-radius: 20px !important;
        border: 2px dashed rgba(224, 122, 95, 0.4) !important;
        padding: 16px !important;
        box-shadow: inset 3px 3px 6px rgba(180, 165, 150, 0.3), inset -3px -3px 6px #FFFFFF !important;
    }
    [data-testid="stFileUploader"] button {
        background: #E07A5F !important; /* Soft Apricot accent */
        color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 4px 4px 10px rgba(180, 165, 150, 0.35) !important;
        transition: transform 0.2s cubic-bezier(0.68, -0.55, 0.27, 1.55) !important;
    }
    [data-testid="stFileUploader"] button:hover {
        transform: scale(1.04) !important;
        background: #d0694e !important;
    }
    [data-testid="stFileUploader"] button:active {
        transform: scale(0.96) !important;
    }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
        color: #2C2825 !important; /* Crisp dark text */
        font-weight: 600 !important;
    }
    
    /* Uploaded file chip background and text color inside st.file_uploader */
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
        background-color: #E8E0D8 !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: inset 2px 2px 5px rgba(180, 165, 150, 0.3), inset -2px -2px 5px #FFFFFF !important;
        padding: 8px 12px !important;
    }
    /* Force high-contrast dark text on file name and file size */
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] div,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] span,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] small {
        color: #1A1817 !important;
        font-weight: 700 !important;
    }

    /* ── Puffy Bouncy Buttons ──────────────────────────────────────────── */
    .stButton > button {
        background: var(--bg-card) !important;
        border: none !important;
        border-radius: 40px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 2rem !important;
        color: var(--text-dark) !important;
        box-shadow: var(--clay-sidebar-out) !important;
        transition: var(--bounce) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
    }

    .stButton > button:active {
        transform: scale(0.96) !important;
        box-shadow: inset 4px 4px 8px rgba(180, 165, 150, 0.4) !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--apricot) !important;
        color: #ffffff !important;
        box-shadow: 6px 6px 14px rgba(224, 122, 95, 0.4), -6px -6px 14px #FFFFFF, inset 2px 2px 6px rgba(255,255,255,0.4), inset -2px -2px 6px rgba(0,0,0,0.1) !important;
    }
    .stButton > button[kind="primary"] * {
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"]:active {
        box-shadow: inset 6px 6px 12px rgba(0,0,0,0.2) !important;
    }

    /* ── Top Navigation Bar (SaaS Layout) ──────────────────────────────── */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 2rem;
        margin-bottom: 2rem;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-dark);
    }
    .nav-brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 16px;
        background: var(--mint);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        box-shadow: var(--clay-out), var(--clay-in);
    }
    .nav-status {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 20px;
        border-radius: 30px;
        background: var(--mint);
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 700;
        box-shadow: var(--clay-out), var(--clay-in);
    }
    .status-dot-nav {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #ffffff;
        box-shadow: 0 0 10px rgba(255,255,255,0.8);
    }
    .nav-links {
        display: flex;
        align-items: center;
        gap: 15px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .nav-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 20px;
        border-radius: 30px;
        background: var(--mint);
        color: #ffffff !important;
        text-decoration: none;
        transition: var(--bounce);
        box-shadow: var(--clay-sidebar-out);
        cursor: pointer;
    }
    .nav-btn:hover {
        transform: translateY(-3px);
    }
    .nav-btn:active {
        transform: scale(0.96);
    }
    .nav-btn * {
        color: #ffffff !important;
    }

    /* ── Hero Section (2-Column Left Aligned) ──────────────────────────── */
    .hero-eyebrow {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        background: var(--yellow);
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        box-shadow: var(--clay-out), var(--clay-in);
        color: #8c7314;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        color: var(--text-dark) !important;
        text-shadow: none !important;
    }
    .hero-body {
        font-size: 1.2rem;
        line-height: 1.6;
        color: var(--text-muted);
        margin-bottom: 2.5rem;
        max-width: 90%;
    }
    
    /* ── Right Column Tactile Mockup ───────────────────────────────────── */
    .mockup-card {
        background: var(--bg-card);
        border-radius: 40px;
        padding: 2.5rem;
        box-shadow: var(--clay-out), var(--clay-in);
        max-width: 100%;
        margin: 0 auto;
        transform: rotate(2deg);
        transition: var(--bounce);
    }
    .mockup-card:hover {
        transform: rotate(0deg) translateY(-3px);
    }
    .mockup-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .mockup-score {
        background: var(--mint);
        color: #ffffff;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.2rem;
        box-shadow: var(--clay-sidebar-out), var(--clay-in);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .mockup-doc {
        font-family: 'IBM Plex Mono', monospace;
        background: var(--bg-main);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: inset 4px 4px 8px rgba(180,165,150,0.4), inset -4px -4px 8px #FFFFFF;
        font-size: 0.9rem;
        line-height: 1.5;
        color: var(--text-muted);
    }

    /* ── Feature Cards (Left Aligned with Accent) ──────────────────────── */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-bottom: 4rem;
        margin-top: 4rem;
    }
    .clay-feature {
        background: var(--bg-card);
        border-radius: 35px;
        padding: 2.5rem 2rem;
        box-shadow: var(--clay-out), var(--clay-in);
        text-align: left;
        position: relative;
        overflow: hidden;
        transition: var(--bounce);
    }
    .clay-feature:hover {
        transform: translateY(-3px);
    }
    .clay-feature:active {
        transform: scale(0.96);
    }
    .feature-accent-1 { border-left: 10px solid var(--apricot); }
    .feature-accent-2 { border-left: 10px solid var(--mint); }
    .feature-accent-3 { border-left: 10px solid var(--yellow); }
    
    .clay-icon-large {
        width: 64px;
        height: 64px;
        border-radius: 20px;
        background: var(--bg-main);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-dark);
        margin-bottom: 1.5rem;
        box-shadow: var(--clay-sidebar-out), var(--clay-in);
    }
    .clay-feature h3 {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    .clay-feature p {
        font-size: 1rem;
        line-height: 1.6;
    }

    /* ── Tabs (Physical Segmented Controller) ──────────────────────────── */
    /* Style tab bar container as a pill-shaped clay controller */
    [data-baseweb="tab-list"] {
        background-color: #E8E0D8 !important;
        border-radius: 30px !important;
        padding: 6px !important;
        gap: 8px !important;
        box-shadow: inset 3px 3px 6px rgba(180, 165, 150, 0.35), inset -3px -3px 6px #FFFFFF !important;
        border: none !important;
    }

    /* Individual tab buttons */
    [data-baseweb="tab"] {
        border-radius: 20px !important;
        padding: 8px 20px !important;
        color: #7A7268 !important;
        font-weight: 700 !important;
        border: none !important;
        background-color: transparent !important;
    }

    /* Active selected tab */
    [data-baseweb="tab"][aria-selected="true"] {
        background-color: #F0EBE4 !important;
        color: #1A1817 !important;
        box-shadow: 4px 4px 10px rgba(180, 165, 150, 0.3), -4px -4px 10px #FFFFFF !important;
    }

    /* Hide Streamlit's default active tab red underline */
    [data-baseweb="tab-highlight-title"], [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ── Chat / Main Workspace ─────────────────────────────────────────── */
    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        border-radius: 30px;
        margin-bottom: 1.25rem;
        background: var(--bg-card);
        box-shadow: var(--clay-sidebar-out);
        border: none;
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background: var(--bg-main);
        box-shadow: inset 4px 4px 8px rgba(180, 165, 150, 0.4), inset -4px -4px 8px #FFFFFF;
    }
    [data-testid="stChatMessage"] * { color: var(--text-dark) !important; }

    [data-testid="stExpander"] {
        border: none !important;
        border-radius: 24px !important;
        background: var(--bg-main) !important;
        box-shadow: inset 4px 4px 8px rgba(180, 165, 150, 0.4), inset -4px -4px 8px #FFFFFF !important;
        margin-top: 1rem;
    }
    [data-testid="stExpander"] summary {
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text-dark) !important;
    }

    /* ── Puffy File Chips & Status Cards ───────────────────────────────── */
    .status-card-puffy {
        background: var(--bg-card);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: var(--clay-out), var(--clay-in);
        text-align: center;
        transition: var(--bounce);
    }
    .status-card-puffy:hover {
        transform: translateY(-3px);
    }
    .status-card-puffy:active {
        transform: scale(0.96);
    }

    .file-chip {
        display: flex;
        align-items: center;
        gap: 12px;
        background: var(--bg-card);
        padding: 12px 20px;
        border-radius: 30px;
        box-shadow: var(--clay-sidebar-out);
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    .file-chip-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--mint);
        box-shadow: 0 0 8px var(--mint);
    }

    /* ── Footer Terms & Conditions ─────────────────────────────────────── */
    .footer-terms {
        text-align: center;
        padding: 2rem;
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 4rem;
        font-weight: 600;
    }

    /* ── Hide Defaults ─────────────────────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
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
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True
if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []

# ─── Helper: Generate base64 data URIs for local files ────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _pdf_data_uri(filename):
    """Read a local PDF and return a base64 data URI that opens in a new tab."""
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:application/pdf;base64,{b64}"
    return "#"

def _md_to_html_data_uri(filename, title="Document"):
    """Read a local .md file, convert to styled HTML, and return a base64 data URI."""
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()
        html_body = md_lib.markdown(md_content, extensions=["fenced_code", "tables"])
        full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; color: #2C2825; line-height: 1.7; }}
  h1, h2, h3 {{ color: #1A1817; }} code {{ background: #f0ebe4; padding: 2px 6px; border-radius: 4px; }}
  pre {{ background: #f0ebe4; padding: 1rem; border-radius: 12px; overflow-x: auto; }}
</style></head><body>{html_body}</body></html>"""
        b64 = base64.b64encode(full_html.encode("utf-8")).decode()
        return f"data:text/html;base64,{b64}"
    return "#"

# Pre-compute data URIs at startup so they're available for the HTML templates
DOCS_URI = _md_to_html_data_uri("agents.md", "Sentinel AI — Docs")
ARCH_URI = _md_to_html_data_uri("ARCHITECTURE.md", "Sentinel AI — Architecture")
TERMS_URI = _pdf_data_uri("Sentinel_AI_Terms_and_Conditions_Professional.pdf")
PRIVACY_URI = _pdf_data_uri("Sentinel_AI_Privacy_Policy_Professional.pdf")

def enter_workspace():
    st.session_state.show_landing = False

def go_home():
    st.session_state.show_landing = True

# ─── Dynamic UI Hiding ────────────────────────────────────────────────────────
if st.session_state.show_landing:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ─── Sidebar (Workspace Only) ─────────────────────────────────────────────────
if not st.session_state.show_landing:
    with st.sidebar:
        st.markdown("<div style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
        if st.button("← Back to Landing Page", use_container_width=True, on_click=go_home):
            pass
        st.markdown("</div>", unsafe_allow_html=True)
            
        # Clean horizontal brand row
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 8px 4px 20px 4px;">
            <div style="width: 38px; height: 38px; border-radius: 12px; background: #E07A5F; display: flex; align-items: center; justify-content: center; box-shadow: 3px 3px 8px rgba(180,165,150,0.4);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #1A1817; line-height: 1.1;">Sentinel AI</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #7A7268; letter-spacing: 0.05em; margin-top: 2px;">WORKSPACE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Upload enterprise documents",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
        if st.button("Process Documents", type="primary", use_container_width=True):
            if uploaded_files:
                with st.spinner("Indexing documents..."):
                    raw_docs = process_uploaded_files(uploaded_files)
                    chunks = get_text_chunks(raw_docs)
                    
                    if not chunks:
                        st.error("Could not extract readable text from the uploaded PDF/document. Please upload a valid document with selectable text.")
                    else:
                        st.session_state.processed_chunks = chunks

                        vectorstore = build_vectorstore(chunks)
                        st.session_state.retriever = get_retriever(vectorstore)
                        st.session_state.rag_chain = create_sentinel_rag_chain(st.session_state.retriever)

                        st.session_state.file_count = len(uploaded_files)
                        st.session_state.chunk_count = len(chunks)
                        st.session_state.uploaded_file_names = [f.name for f in uploaded_files]
                        
                        st.success("Indexing complete.")
                        time.sleep(0.5)
                        st.rerun()
            else:
                st.warning("Please upload a document first.")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.file_count > 0:
            st.markdown(f"""
            <div style="margin-top: 2rem; font-weight: 800; margin-bottom: 1rem; font-size: 1.1rem; text-align: center;">Active Documents</div>
            """, unsafe_allow_html=True)
            for fname in st.session_state.uploaded_file_names:
                st.markdown(f"""
                <div class="file-chip">
                    <div class="file-chip-dot"></div>
                    <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">{fname}</div>
                </div>
                """, unsafe_allow_html=True)

# ─── Landing Page View ────────────────────────────────────────────────────────
if st.session_state.show_landing:
    # Top Navigation Bar
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">
            <div class="nav-brand-icon">{ICONS['shield']}</div>
            Sentinel AI
        </div>
        <div class="nav-status">
            <div class="status-dot-nav"></div>
            System Operational
        </div>
        <div class="nav-links">
            <a href="{DOCS_URI}" target="_blank" class="nav-btn">{ICONS['book']} Docs</a>
            <a href="{ARCH_URI}" target="_blank" class="nav-btn">{ICONS['layer']} Architecture</a>
            <a href="https://github.com/sritamcodes/Sentinel-AI.git" target="_blank" class="nav-btn">{ICONS['github']} GitHub Repo</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Asymmetrical 2-Column Hero
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="padding-top: 2rem;">
            <div class="hero-eyebrow">Enterprise Compliance Intelligence</div>
            <h1 class="hero-title">Automated Policy Verification & Citation Auditing</h1>
            <p class="hero-body">Transform static compliance manuals into verifiable intelligence. Run line-by-line risk audits and grounded Q&A with zero hallucination guarantee.</p>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns([1, 1.5])
        with btn_col1:
            if st.button("Enter Workspace →", type="primary", use_container_width=True, on_click=enter_workspace):
                pass
            
    with col2:
        st.markdown(f"""
        <div class="mockup-card">
            <div class="mockup-header">
                <div style="font-weight: 800; font-size: 1.2rem;">Audit Report</div>
                <div class="mockup-score">
                    <div style="width: 20px; height: 20px;">{ICONS['check']}</div> 98% Compliant
                </div>
            </div>
            <div style="font-weight: 700; margin-bottom: 0.5rem; color: var(--text-dark);">Verified Source Citation:</div>
            <div class="mockup-doc">
                "All external vendors must undergo a tier-1 security review before receiving access to production databases. Refer to section 4.2.1."<br><br>
                <span style="color: var(--mint); font-weight: 800;">[Source: Vendor_Policy_2024.pdf, Page 12]</span>
            </div>
            <div style="margin-top: 1.5rem; display: flex; gap: 10px;">
                <div style="height: 12px; width: 60%; background: var(--apricot); border-radius: 10px;"></div>
                <div style="height: 12px; width: 30%; background: var(--mint); border-radius: 10px;"></div>
            </div>
            <div style="margin-top: 10px; display: flex; gap: 10px;">
                <div style="height: 12px; width: 40%; background: var(--bg-main); border-radius: 10px;"></div>
                <div style="height: 12px; width: 50%; background: var(--yellow); border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Cards Showcase
    st.markdown(f"""
    <div class="features-grid">
        <div class="clay-feature feature-accent-1">
            <div class="clay-icon-large">{ICONS['book']}</div>
            <h3>Grounded RAG</h3>
            <p>Synthesizes answers directly from uploaded policy manuals with zero hallucination guarantee.</p>
        </div>
        <div class="clay-feature feature-accent-2">
            <div class="clay-icon-large">{ICONS['search']}</div>
            <h3>Compliance Risk Audit</h3>
            <p>Automatically flags non-compliant clauses and identifies operational policy gaps.</p>
        </div>
        <div class="clay-feature feature-accent-3">
            <div class="clay-icon-large">{ICONS['check']}</div>
            <h3>Citation Tracing</h3>
            <p>Every output includes verifiable source citations pointing directly to exact document sections.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
# ─── Main Workspace View ──────────────────────────────────────────────────────
else:
    is_active = st.session_state.rag_chain is not None
    
    if not is_active:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 1.2rem; font-weight: 700; color: #1A1817;">Workspace Ready</div>
            <p style="color: #7A7268; margin-top: 6px;">Upload a PDF document in the sidebar to begin running compliance audits.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        tab_chat, tab_audit = st.tabs(["Document Q&A", "Risk Audit"])

        # ── Tab 1: Intelligence Chat ──────────────────────────────────────────
        with tab_chat:
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

            for msg in st.session_state.chat_history:
                # Using generic string for avatar inside st.chat_message since Streamlit doesn't render SVG properly in the avatar parameter
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant" and "sources" in msg:
                        with st.expander("View Source Citations"):
                            for src in msg["sources"]:
                                st.markdown(f"""
                                <div style="background: var(--bg-card); padding: 1.5rem; border-radius: 20px; box-shadow: var(--clay-sidebar-out); margin-bottom: 1rem;">
                                    <div style="font-family: 'IBM Plex Mono', monospace; font-weight: 700; color: var(--apricot); margin-bottom: 0.5rem;">
                                        Source [{src['idx']}] • {src['file']} (Page {src['page']})
                                    </div>
                                    <div style="line-height: 1.6;">{src['content'][:400]}{'...' if len(src['content']) > 400 else ''}</div>
                                </div>
                                """, unsafe_allow_html=True)

            if user_query := st.chat_input("Query your document index..."):
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                with st.chat_message("user"):
                    st.markdown(user_query)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing index..."):
                        response = st.session_state.rag_chain.invoke(user_query)
                        st.markdown(response)

                        sources = []
                        if st.session_state.retriever:
                            retrieved_docs = st.session_state.retriever.invoke(user_query)
                            with st.expander("View Source Citations"):
                                for idx, doc in enumerate(retrieved_docs, start=1):
                                    src_file = doc.metadata.get("source", "Unknown")
                                    src_page = doc.metadata.get("page", "N/A")
                                    content = doc.page_content
                                    sources.append({"idx": idx, "file": src_file, "page": src_page, "content": content})
                                    st.markdown(f"""
                                    <div style="background: var(--bg-card); padding: 1.5rem; border-radius: 20px; box-shadow: var(--clay-sidebar-out); margin-bottom: 1rem;">
                                        <div style="font-family: 'IBM Plex Mono', monospace; font-weight: 700; color: var(--apricot); margin-bottom: 0.5rem;">
                                            Source [{idx}] • {src_file} (Page {src_page})
                                        </div>
                                        <div style="line-height: 1.6;">{content[:400]}{'...' if len(content) > 400 else ''}</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })

        # ── Tab 2: Compliance Audit ───────────────────────────────────────────
        with tab_audit:
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: var(--bg-card); padding: 2.5rem; border-radius: 35px; box-shadow: var(--clay-out), var(--clay-in); display: flex; gap: 2rem; align-items: center; margin-bottom: 2rem; border-left: 10px solid var(--mint);">
                <div style="width: 80px; height: 80px; border-radius: 24px; background: var(--bg-main); display: flex; align-items: center; justify-content: center; color: var(--text-dark); flex-shrink: 0; box-shadow: var(--clay-sidebar-out), var(--clay-in);">
                    {ICONS['search']}
                </div>
                <div>
                    <h2 style="margin-bottom: 0.5rem; font-weight: 800;">Automated Risk Audit</h2>
                    <p style="font-size: 1.1rem;">Execute an autonomous evaluation across all indexed documents to identify policy gaps and risk vectors.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Run Full Audit", type="primary", use_container_width=True):
                with st.spinner("Evaluating compliance guidelines..."):
                    report = run_compliance_audit(st.session_state.processed_chunks)
                    st.markdown(f"""
                    <div style="background: var(--bg-card); padding: 2.5rem; border-radius: 35px; box-shadow: var(--clay-out), var(--clay-in); margin-top: 1.5rem;">
                        {report}
                    </div>
                    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-terms">
    © 2026 Sentinel AI. Playful. Verified. Secure.<br>
    <a href="{TERMS_URI}" target="_blank" style="color: var(--mint); text-decoration: none;">Terms & Conditions</a> • <a href="{PRIVACY_URI}" target="_blank" style="color: var(--mint); text-decoration: none;">Privacy Policy</a>
</div>
""", unsafe_allow_html=True)