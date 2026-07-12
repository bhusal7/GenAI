# 📚 Research Paper ChatBox

An AI-powered Research Paper Question Answering application built using LangChain, ChromaDB, HuggingFace Embeddings, and Mistral AI.

The assistant retrieves the most relevant sections from a research paper and answers questions strictly from the provided document.

---

## 🚀 Features

- 📄 Research Paper Question Answering
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 HuggingFace Embeddings
- 💾 Chroma Vector Database
- 🎯 MMR (Max Marginal Relevance) Retrieval
- 🤖 Mistral Large Language Model
- 💬 Interactive Command-Line Chat Interface
- 📑 Displays Retrieved Chunks
- ❌ Prevents Hallucinations by Answering Only from Context

---

## 🛠 Tech Stack

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Mistral AI
- dotenv

---

## 📂 Project Structure

```
Research_Paper_ChatBox/
│
├── app.py
├── chroma_db/
├── research_paper.pdf
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Pipeline

```
Research Paper PDF
        ↓
Vector Database (ChromaDB)
        ↓
Retriever (MMR Search)
        ↓
Relevant Chunks
        ↓
Prompt Template
        ↓
Mistral AI
        ↓
Accurate Answer
```

---

## 📋 Installation

```bash
git clone <repository-url>

cd Research_Paper_ChatBox

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```
MISTRAL_API_KEY=your_api_key
```

---

## ▶️ Run

```bash
python main.py
```

---

## 💬 Example Questions

- What is the main objective of this research?
- What methodology is used?
- What datasets were used?
- What are the key findings?
- What future work is suggested?

---

## 📌 Output

- Retrieves the most relevant document chunks
- Sends only those chunks to the LLM
- Generates concise and context-aware answers

---

## 📚 Built With

- LangChain
- ChromaDB
- HuggingFace Embeddings
- Mistral AI

---

## 👨‍💻 Author

Bashudev Bhusal