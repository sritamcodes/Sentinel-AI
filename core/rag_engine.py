from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os


def get_groq_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0) -> ChatGroq:
    """Return a configured ChatGroq LLM instance.
    Key is read lazily at call-time so it is always resolved after load_dotenv().
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file and restart the app."
        )
    return ChatGroq(model=model, temperature=temperature, api_key=api_key)


def create_sentinel_rag_chain(retriever):
    # Read key at call-time (after load_dotenv() in app.py has already run)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file and restart the app."
        )
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)

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