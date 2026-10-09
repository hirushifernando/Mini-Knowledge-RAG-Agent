from langchain_core.output_parsers import StrOutputParser

from src.prompts import RAG_PROMPT


def create_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


def retrieve_documents(retriever, question: str):
    return retriever.invoke(question)


def answer_question(question: str, retriever, llm):
    documents = retrieve_documents(retriever, question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    chain = RAG_PROMPT | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": question
    })

    sources = list(dict.fromkeys(
        document.metadata.get("source", "Unknown")
        for document in documents
    ))

    return {
        "answer": answer,
        "sources": sources
    }