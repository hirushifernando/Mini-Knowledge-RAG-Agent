
from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful knowledge assistant.

Answer the user's question using the provided context.

Rules:
- Use the context when answering.
- Do not invent information.
- If the answer is not available in the context,
  clearly say that you could not find it in the documents.
- Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""
)


SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """
Summarize the following document content.

Rules:
- Keep the main ideas and important concepts.
- Remove unnecessary repetition.
- Use clear headings and bullet points when useful.
- Do not add information that is not in the text.

Document content:
{text}

Summary:
"""
)


EXPLAIN_PROMPT = ChatPromptTemplate.from_template(
    """
Explain the following document content in simple English.

Rules:
- Use short, clear sentences.
- Explain technical words simply.
- Include a short example if useful.
- Keep the explanation accurate to the provided content.
- Do not invent facts.

Document content:
{text}

Simple explanation:
"""
)