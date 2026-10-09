
from src.rag import retrieve_documents, answer_question


def search_documents(question: str, retriever):
    """Search the user's documents through the retriever."""
    return retrieve_documents(retriever, question)


def generate_answer(question: str, llm):
    """Answer a general question directly using the LLM."""
    response = llm.invoke(question)
    return response.content


def run_agent(question: str, retriever, llm):
    """
    Route questions to document RAG or a general LLM answer.
    """

    document_keywords = [
        "my document",
        "my documents",
        "uploaded document",
        "uploaded documents",
        "according to the document",
        "according to my documents",
        "in my file",
        "in my files",
        "what does my",
        "based on the document",
        "from the document"
    ]

    question_lower = question.lower()

    use_rag = any(
        keyword in question_lower
        for keyword in document_keywords
    )

    if use_rag:
        result = answer_question(
            question,
            retriever,
            llm
        )

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "route": "RAG"
        }

    answer = generate_answer(question, llm)

    return {
        "answer": answer,
        "sources": [],
        "route": "Direct LLM"
    }