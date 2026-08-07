from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq  # Or langchain_openai / ChatOllama depending on your LLM


def get_groq_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0) -> ChatGroq:
    """Return a configured ChatGroq LLM instance."""
    return ChatGroq(model=model, temperature=temperature)


def create_sentinel_rag_chain(retriever):
    # Initialize your LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # Prompt Template
    system_prompt = (
        "You are Sentinel AI, an enterprise compliance and knowledge assistant.\n"
        "Answer the user's question using ONLY the provided context below.\n"
        "If the answer is not in the context, state clearly that the document does not contain that information.\n\n"
        "Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Helper function to format retrieved documents
    def format_docs(docs):
        return "\n\n".join(f"[{doc.metadata.get('source', 'Doc')}]: {doc.page_content}" for doc in docs)

    # Modern LCEL Chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain