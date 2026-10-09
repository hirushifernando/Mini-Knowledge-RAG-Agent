
from dotenv import load_dotenv

from src.document_loader import load_documents, split_documents
from src.embeddings import create_embeddings
from src.vector_store import create_vector_store
from src.llm import create_llm
from src.rag import create_retriever
from src.agent import run_agent

load_dotenv()

print("Loading documents...")
documents = load_documents("data/documents")
chunks = split_documents(documents)

print("Creating vector database...")
embeddings = create_embeddings()
vector_store = create_vector_store(chunks, embeddings)
retriever = create_retriever(vector_store)

print("Connecting to Groq...")
llm = create_llm()

questions = [
    "What does my ML document say about classification?",
    "What is artificial intelligence?"
]

for question in questions:
    print("\n" + "=" * 50)
    print("Question:", question)

    result = run_agent(question, retriever, llm)

    print("Route:", result["route"])
    print("Answer:", result["answer"])

    if result["sources"]:
        print("Sources:", result["sources"])