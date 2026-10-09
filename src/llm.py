import os

from langchain_groq import ChatGroq


def create_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it to your .env file."
        )

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )