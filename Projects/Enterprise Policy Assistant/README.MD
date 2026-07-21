# 🏢 Company Policy RAG Assistant

An AI-powered Company Policy Assistant built using LangChain, ChromaDB, HuggingFace Embeddings, and Mistral AI.

The assistant answers employee questions by retrieving relevant company policy documents and generating responses strictly from the provided context.

---

## 🚀 Features

- 📄 Company Policy Question Answering
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 HuggingFace Embeddings
- 💾 Chroma Vector Database
- 🎯 MMR (Max Marginal Relevance) Retrieval
- 🤖 Mistral Large Language Model
- 💬 Interactive Command-Line Chat Interface
- 📑 Displays Retrieved Chunks
- ❌ Prevents Hallucinations by Restricting Answers to Company Policy

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
Company_Policy_RAG_Assistant/
│
├── app.py
├── chroma_db/
├── company_policy.pdf
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Pipeline

```
Company Policy PDF
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
Policy-Based Answer
```

---

## 📋 Installation

```bash
git clone <repository-url>

cd Company_Policy_RAG_Assistant

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

- What is the company's leave policy?
- How should employees report incidents?
- What are the working hours?
- What is the remote work policy?
- What is the code of conduct?

---

## 📌 Output

- Retrieves the most relevant policy sections
- Uses only the retrieved policy context
- Generates accurate and reliable answers
- Returns:

```
I don't know based on the provided company policy.
```

when the answer is unavailable.

---

## 📚 Built With

- LangChain
- ChromaDB
- HuggingFace Embeddings
- Mistral AI

---

## 👨‍💻 Author

Bashudev Bhusal