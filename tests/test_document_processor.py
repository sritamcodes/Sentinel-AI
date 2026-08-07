from langchain_core.documents import Document
from core.document_processor import get_text_chunks

def test_chunking_preserves_metadata():
    sample_docs = [
        Document(
            page_content="This is a test enterprise document page content. " * 50,
            metadata={"source": "test_policy.pdf", "page": 1}
        )
    ]
    chunks = get_text_chunks(sample_docs)
    assert len(chunks) > 0
    assert chunks[0].metadata["source"] == "test_policy.pdf"
    assert chunks[0].metadata["page"] == 1