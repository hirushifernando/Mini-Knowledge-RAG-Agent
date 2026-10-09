# Mini Knowledge RAG Agent 🤖

A lightweight AI-powered research assistant that helps users understand their documents through question answering, summarization, and simple explanations. Built with Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), Hugging Face embeddings, FAISS vector search, and Streamlit.

## 🚀 Project Overview

Mini Knowledge RAG Agent allows users to upload text documents and interact with their content using natural language.

Instead of relying only on an LLM's general knowledge, the application retrieves relevant information from the uploaded documents and uses it as context to generate answers.

The project also includes document summarization, simple explanations, and a lightweight keyword-based routing system that directs questions to document retrieval or direct LLM responses.

## ✨ Key Features

* **📄 Document Upload:** Upload multiple `.txt` files to create a personal knowledge base.
* **🔍 Semantic Search:** Find relevant document sections using vector embeddings and FAISS.
* **💬 RAG Question Answering:** Generate answers grounded in retrieved document content.
* **📝 Text Summarization:** Produce concise summaries of uploaded documents.
* **💡 Simple Explanations:** Explain technical concepts and document content in simple English.
* **🧠 LLM Integration:** Use a hosted Groq API model without running a large language model locally.
* **🔢 Text Embeddings:** Convert document chunks into numerical vectors for semantic retrieval.
* **🎯 Prompt Engineering:** Use task-specific prompts for question answering, summarization, and explanations.
* **🤖 Simple Agent Routing:** Route document-related questions to RAG and other questions to the LLM using keyword-based rules.
* **🖥️ Interactive UI:** Use the application through a Streamlit web interface.
* **💻 Lightweight Design:** Run the application on a CPU without requiring a dedicated GPU for LLM inference.

## 🛠️ Technologies Used

| Technology                          | Purpose                                             |
| ----------------------------------- | --------------------------------------------------- |
| Python                              | Core programming language                           |
| Streamlit                           | Interactive web interface                           |
| LangChain                           | LLM integration and RAG workflow                    |
| Groq API                            | Hosted LLM inference                                |
| Hugging Face Transformers ecosystem | Access to pretrained NLP models and embedding tools |
| Sentence Transformers               | Generate text embeddings                            |
| `all-MiniLM-L6-v2`                  | Lightweight sentence embedding model                |
| FAISS                               | Vector similarity search                            |
| Recursive Character Text Splitter   | Split documents into manageable chunks              |
| python-dotenv                       | Load environment variables securely                 |
| Jupyter Notebook                    | Experiment with embeddings, retrieval, and prompts  |
| Git & GitHub                        | Version control and project hosting                 |

## 🏗️ System Architecture

```text
          User
           |
           v
     Streamlit UI
           |
           v
   Upload Text Documents
           |
           v
   Document Processing
   (Loading and Chunking)
           |
           v
   Generate Embeddings
           |
           v
    FAISS Vector Store
           |
           v
     User's Question
           |
           v
    Keyword-Based Router
       /           \
      v             v
 Document RAG    Direct LLM
      |             |
      v             |
 Retrieve Relevant  |
 Document Chunks    |
      |             |
      v             |
   Build Prompt     |
       \            /
        v          v
         Groq LLM
            |
            v
      Generated Answer
```

For summarization and simple explanations, the application sends the selected document content to the LLM using a task-specific prompt.

## 🔄 How RAG Works

1. **Load:** Read the uploaded text documents.
2. **Split:** Divide the documents into smaller text chunks.
3. **Embed:** Convert each chunk into a numerical vector using `all-MiniLM-L6-v2`.
4. **Index:** Store the vectors in a FAISS vector store.
5. **Retrieve:** Search for the most relevant chunks when the user asks a question.
6. **Augment:** Add the retrieved content to the question prompt.
7. **Generate:** Send the prompt to the hosted LLM and display the answer.

This workflow helps the LLM answer questions using the available document context.

## 📂 Project Structure

```text
Mini-Knowledge-RAG-Agent/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── src/
│   ├── agent.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── prompts.py
│   ├── rag.py
│   └── vector_store.py
│
├── data/
│   └── documents/
│       ├── machine_learning.txt
│       ├── deep_learning.txt
│       └── nlp.txt
│
├── notebooks/
│   └── mini_rag_experiments.ipynb
│
├── test_agent.py
└── test_rag.py
```

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.10 or later, compatible with the installed dependencies
* Git
* A Groq API key
* Internet access for the hosted LLM and initial model download

### 1. Clone the Repository

```bash
git clone https://github.com/hirushifernando/Mini-Knowledge-RAG-Agent.git
cd Mini-Knowledge-RAG-Agent
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own API key from the Groq Console.

**Security:** Never commit your `.env` file or expose your API key in source code, screenshots, filenames, or public repositories.

### 5. Run the Application

```powershell
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

## 🧪 Example Use Cases

### Ask Questions

Upload a document and ask:

* "What is deep learning according to my document?"
* "Explain the main concepts discussed in my files."
* "What are the key differences between machine learning and deep learning?"

### Summarize Documents

Choose **Summarize** to generate a concise summary of the selected document content.

### Explain Simply

Choose **Explain Simply** to receive an easy-to-understand explanation of technical material.

### Direct LLM Questions

Ask a general question to use the direct LLM route instead of document retrieval.

*Note: Direct LLM answers may use the model's general knowledge rather than your uploaded documents.*

## 🔬 Experiments

The Jupyter notebook explores:

* Document loading and text chunking
* Generating text embeddings
* Building a FAISS vector store
* Retrieving relevant document chunks
* Comparing retrieval results for different values of `k`
* Experimenting with prompts and LLM responses
* Visualizing retrieval behavior and embedding representations

## ⚠️ Current Limitations

* Supports `.txt` documents in the current implementation.
* Uses keyword-based routing rather than an autonomous, tool-using agent.
* Answer quality depends on document content, retrieval relevance, and the LLM.
* The vector store is held in application session memory and is not automatically preserved after restarting the app.
* Summarization and explanation are limited to a maximum input length in the current implementation.
* Hosted LLM usage requires an internet connection and a valid API key.
* Generated answers can still contain errors; important information should be verified against the source documents.

## 🔮 Future Improvements

* Support PDF and DOCX document uploads.
* Add persistent vector storage.
* Display source excerpts and retrieval relevance scores.
* Improve agent routing with an LLM-based decision process.
* Add chat history and follow-up questions.
* Evaluate retrieval quality and answer faithfulness.
* Deploy the application for public access.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Large Language Model integration
* Text embeddings and semantic search
* Vector databases and FAISS
* Prompt engineering
* Document preprocessing and chunking
* LangChain-based workflows
* Lightweight AI application development
* Streamlit UI development
* API configuration and environment variable management

## 👩‍💻 Author

**Hirushi Fernando**

Computer Science Graduate | AI/ML | Data Science | Generative AI

---

⭐ If you find this project interesting, consider giving the repository a star!
