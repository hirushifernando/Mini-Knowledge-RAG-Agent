
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from src.document_loader import split_documents
from src.embeddings import create_embeddings
from src.vector_store import create_vector_store
from src.llm import create_llm
from src.rag import create_retriever, answer_question
from src.agent import run_agent
from src.prompts import SUMMARY_PROMPT, EXPLAIN_PROMPT



st.set_page_config(
    page_title="Mini Knowledge RAG Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mini Knowledge RAG Agent")

st.write(
    "Upload knowledge documents, ask questions, "
    "summarize content, or get simple explanations."
)

# Store the knowledge base between Streamlit reruns.
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "document_texts" not in st.session_state:
    st.session_state.document_texts = {}

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []


# -------------------------------
# 1. Upload documents
# -------------------------------

st.header("📚 Knowledge Documents")

uploaded_files = st.file_uploader(
    "Upload TXT documents",
    type=["txt"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Selected files: {len(uploaded_files)}")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")


# -------------------------------
# 2. Build knowledge base
# -------------------------------

if st.button("🔨 Build Knowledge Base", type="primary"):
    if not uploaded_files:
        st.warning("Please upload at least one TXT document.")
    else:
        try:
            documents = []
            document_texts = {}

            for file in uploaded_files:
                text = file.getvalue().decode("utf-8-sig")

                if not text.strip():
                    st.warning(f"{file.name} is empty.")
                    continue

                document_texts[file.name] = text

                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": file.name}
                    )
                )

            if not documents:
                st.error("No readable text documents were found.")
            else:
                with st.spinner(
                    "Splitting documents and building the knowledge base..."
                ):
                    chunks = split_documents(documents)
                    embeddings = create_embeddings()
                    vector_store = create_vector_store(
                        chunks,
                        embeddings
                    )

                    st.session_state.retriever = create_retriever(
                        vector_store
                    )

                    st.session_state.document_texts = document_texts
                    st.session_state.indexed_files = list(
                        document_texts.keys()
                    )

                st.success(
                    f"Knowledge base ready! "
                    f"{len(documents)} documents and "
                    f"{len(chunks)} text chunks indexed."
                )

        except Exception as error:
            st.error(f"Could not build knowledge base: {error}")


# -------------------------------
# 3. Select an AI operation
# -------------------------------

st.divider()
st.header("🤖 AI Assistant")

operation = st.radio(
    "Choose an operation",
    [
        "Ask Question",
        "Summarize",
        "Explain Simply"
    ],
    horizontal=True
)


# -------------------------------
# 4. Ask a question using the agent
# -------------------------------

if operation == "Ask Question":
    question = st.text_input(
        "Ask a question",
        placeholder="What does my document say about classification?"
    )

    if st.button("Ask AI"):
        if not question.strip():
            st.warning("Please enter a question.")

        elif st.session_state.retriever is None:
            st.warning(
                "Upload documents and click Build Knowledge Base first."
            )

        else:
            try:
                with st.spinner("Thinking..."):
                    if st.session_state.llm is None:
                        st.session_state.llm = create_llm()

                    result = run_agent(
                        question,
                        st.session_state.retriever,
                        st.session_state.llm
                    )

                st.subheader("💡 Answer")
                st.markdown(result["answer"])

                st.caption(f"Route used: {result['route']}")

                if result["sources"]:
                    st.subheader("📚 Sources")

                    for source in result["sources"]:
                        st.write(f"- {source}")
                else:
                    st.caption(
                        "This answer was generated without document retrieval."
                    )

            except Exception as error:
                st.error(f"Could not generate an answer: {error}")


# -------------------------------
# 5. Summarize documents
# -------------------------------

elif operation == "Summarize":
    if st.session_state.document_texts:
        summary_source = st.selectbox(
            "Choose a document to summarize",
            ["All uploaded documents"]
            + list(st.session_state.document_texts.keys())
        )

        if st.button("Generate Summary"):
            if summary_source == "All uploaded documents":
                text = "\n\n".join(
                    f"Document: {name}\n{content}"
                    for name, content
                    in st.session_state.document_texts.items()
                )
            else:
                text = st.session_state.document_texts[summary_source]

            # Limit input size to keep API usage manageable.
            text = text[:12000]

            try:
                with st.spinner("Summarizing..."):
                    if st.session_state.llm is None:
                        st.session_state.llm = create_llm()

                    chain = (
                        SUMMARY_PROMPT
                        | st.session_state.llm
                        | StrOutputParser()
                    )

                    summary = chain.invoke({"text": text})

                st.subheader("📝 Summary")
                st.markdown(summary)

                if summary_source == "All uploaded documents":
                    sources = list(
                        st.session_state.document_texts.keys()
                    )
                else:
                    sources = [summary_source]

                st.subheader("📚 Sources")
                for source in sources:
                    st.write(f"- {source}")

            except Exception as error:
                st.error(f"Could not summarize the text: {error}")

    else:
        st.info("Upload TXT documents to summarize them.")


# -------------------------------
# 6. Explain documents simply
# -------------------------------

elif operation == "Explain Simply":
    if st.session_state.document_texts:
        explain_source = st.selectbox(
            "Choose a document to explain",
            ["All uploaded documents"]
            + list(st.session_state.document_texts.keys())
        )

        if st.button("Explain Simply"):
            if explain_source == "All uploaded documents":
                text = "\n\n".join(
                    f"Document: {name}\n{content}"
                    for name, content
                    in st.session_state.document_texts.items()
                )
            else:
                text = st.session_state.document_texts[explain_source]

            text = text[:12000]

            try:
                with st.spinner("Preparing a simple explanation..."):
                    if st.session_state.llm is None:
                        st.session_state.llm = create_llm()

                    chain = (
                        EXPLAIN_PROMPT
                        | st.session_state.llm
                        | StrOutputParser()
                    )

                    explanation = chain.invoke({"text": text})

                st.subheader("💡 Simple Explanation")
                st.markdown(explanation)

                if explain_source == "All uploaded documents":
                    sources = list(
                        st.session_state.document_texts.keys()
                    )
                else:
                    sources = [explain_source]

                st.subheader("📚 Sources")
                for source in sources:
                    st.write(f"- {source}")

            except Exception as error:
                st.error(f"Could not explain the text: {error}")


st.divider()

st.caption(
    "Mini Knowledge RAG Agent | "
    "Streamlit • LangChain • Hugging Face Embeddings • FAISS • Groq"
)