# 📝 Smart Notes Generator using LLM

An AI-powered **Smart Notes Generator** built with **LangChain**, **Mistral AI**, and **Python**. This application reads lecture notes, books, or study materials in PDF format and generates structured study notes, revision notes, summaries, and answers to user questions.

---

## 🚀 Features

* 📄 Read PDF study materials
* ✂️ Automatically split documents into chunks
* 🧠 Generate structured study notes
* 📚 Create revision notes
* 📝 Summarize documents
* 🎯 Extract key concepts
* 📌 Highlight important points
* ❓Answer questions using only the uploaded document
* 💬 Interactive terminal chatbot
* ⚡ Fast and lightweight implementation

---

## 🛠️ Tech Stack

* Python
* LangChain
* Mistral AI
* PyPDFLoader
* RecursiveCharacterTextSplitter
* Python-dotenv

---

## 📂 Project Workflow

```text
Lecture Notes PDF
        │
        ▼
Document Loader
        │
        ▼
Text Chunking
        │
        ▼
Prompt Template
        │
        ▼
Mistral LLM
        │
        ▼
Study Notes
Revision Notes
Summaries
Question Answering
```

---

## 📁 Project Structure

```text
SmartNotesGenerator/
│
├── pythonlearn.pdf
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone <repository-url>

cd SmartNotesGenerator

pip install -r requirements.txt
```

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 💬 Example Prompts

* Generate study notes.
* Create revision notes.
* Summarize this document.
* Extract key concepts.
* Explain the main topics.
* Generate important questions.
* Create concise notes.
* Prepare exam revision notes.
* Explain this document in simple language.
* List important definitions.
* Create chapter-wise notes.
* Generate FAQs from this document.

---

## 📚 Learning Concepts

* Large Language Models (LLMs)
* Prompt Engineering
* PDF Processing
* Document Loading
* Text Chunking
* ChatPromptTemplate
* LangChain Workflows

---

## 🔮 Future Improvements

* Support multiple PDFs
* Flashcard generation
* Quiz generation
* Chapter-wise note generation
* Mind map generation
* Streamlit Web App
* Retrieval-Augmented Generation (RAG)
* Vector Database Integration

---

## ⭐ Author

**Bashudev Bhusal**

Built while learning **Generative AI, LangChain, and Large Language Models (LLMs)**.
