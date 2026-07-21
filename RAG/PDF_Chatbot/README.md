# 📚 PDF RAG Assistant

A Retrieval-Augmented Generation (RAG) application that lets you upload any PDF and chat with it using AI.

The application processes your document by splitting it into chunks, generating embeddings, storing them in a Chroma vector database, retrieving the most relevant context, and generating answers using Mistral AI.

---

## 🚀 Features

- 📄 Upload any PDF document
- ✂️ Automatic document chunking
- 🧠 HuggingFace sentence embeddings
- 🗂️ Chroma Vector Database
- 🔍 MMR (Maximal Marginal Relevance) Retrieval
- 💬 Interactive chat interface with Streamlit
- 🤖 Mistral Large LLM
- 📑 View retrieved context for every response
- ⚡ Fast local vector search

---

## 🏗️ Architecture

```

            PDF
             │
             ▼
      PyPDFLoader
             │
             ▼
RecursiveCharacterTextSplitter
             │
             ▼
 HuggingFace Embeddings
             │
             ▼
      Chroma Vector DB
             │
             ▼
      MMR Retriever
             │
             ▼
       Mistral Large
             │
             ▼
         Final Answer
