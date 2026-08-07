from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from core.rag_engine import get_groq_llm

def run_compliance_audit(documents: List[Document]) -> str:
    """
    Custom Skill: Automatically audits enterprise documentation for 
    operational risks, policy highlights, and compliance status.
    """
    llm = get_groq_llm(temperature=0.2)
    sample_text = "\n\n".join([doc.page_content for doc in documents[:6]])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a Senior Enterprise Compliance Auditor. Analyze the document excerpt below.\n"
         "Generate a concise Compliance Pass/Fail Report detailing:\n"
         "1. Overall Compliance Status (PASS / WARNING / FAIL)\n"
         "2. Identified Operational or Legal Risks\n"
         "3. Key Policy Highlights\n"
         "4. Actionable Recommendations"),
        ("human", "Document Excerpt:\n{text}")
    ])
    
    chain = prompt | llm
    res = chain.invoke({"text": sample_text})
    return res.content