import os
import shutil
from typing import List
import streamlit as st
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import config

@st.cache_resource
def get_embedding_function():
    """
    Cached so HuggingFace bge-small model loads into memory ONCE on startup.
    """
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def build_vectorstore(documents: List[Document]) -> Chroma:
    # 1. Ensure chunks is not empty
    if not documents:
        raise ValueError("No text chunks were provided to build the vectorstore.")

    # 2. Extract string content and filter out empty/None values
    clean_documents = []
    for chunk in documents:
        if isinstance(chunk, Document):
            text = chunk.page_content
            metadata = chunk.metadata
        elif isinstance(chunk, str):
            text = chunk
            metadata = {}
        else:
            continue
            
        if text and isinstance(text, str) and text.strip():
            clean_documents.append(Document(page_content=text.strip(), metadata=metadata))
    
    if not clean_documents:
        raise ValueError("All extracted text chunks were empty or invalid.")

    if os.path.exists(config.CHROMA_PERSIST_DIR):
        try:
            shutil.rmtree(config.CHROMA_PERSIST_DIR)
        except Exception:
            pass

    embeddings = get_embedding_function()
    
    # 3. Build Chroma Vectorstore safely
    vectorstore = Chroma.from_documents(
        documents=clean_documents,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        persist_directory=config.CHROMA_PERSIST_DIR
    )
    return vectorstore

def get_retriever(vectorstore: Chroma, k: int = 4):
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": 10}
    )