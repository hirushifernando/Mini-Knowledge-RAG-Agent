from dotenv import load_dotenv

from src.document_loader import load_documents, split_documents
from src.embeddings import create_embeddings
from src.vector_store import create_vector_store
from src.llm import create_llm
from src.rag import create_retriever, answer_question


load_dotenv()

print("Loading documents...")
documents = load_documents("data/documents")
chunks = split_documents(documents)

print("Creating embeddings and vector database...")
embeddings = create_embeddings()
vector_store = create_vector_store(chunks, embeddings)
retriever = create_retriever(vector_store)

print("Connecting to the language model...")
llm = create_llm()

question = "What is deep learning?"

print("\nQuestion:", question)

result = answer_question(question, retriever, llm)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(source)