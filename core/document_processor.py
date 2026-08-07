import io
from typing import List
from pypdf import PdfReader  # <-- Updated from PyPDF2 to pypdf
import docx
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_uploaded_files(uploaded_files) -> List[Document]:
    """
    Extracts raw text from uploaded files (PDF, DOCX, TXT) while binding
    filename and page metadata for exact citation tracing.
    """
    documents = []

    for file in uploaded_files:
        file_name = file.name
        file_ext = file_name.split(".")[-1].lower()

        if file_ext == "pdf":
            pdf_bytes = io.BytesIO(file.read())
            pdf_reader = PdfReader(pdf_bytes)  # pypdf reader class
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={"source": file_name, "page": page_num}
                        )
                    )

        elif file_ext == "docx":
            doc_bytes = io.BytesIO(file.read())
            doc = docx.Document(doc_bytes)
            full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            if full_text:
                documents.append(
                    Document(
                        page_content=full_text,
                        metadata={"source": file_name, "page": 1}
                    )
                )

        elif file_ext == "txt":
            text = file.read().decode("utf-8")
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": file_name, "page": 1}
                    )
                )

    return documents

def get_text_chunks(documents: List[Document]) -> List[Document]:
    """
    Splits documents into contextual chunks using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)