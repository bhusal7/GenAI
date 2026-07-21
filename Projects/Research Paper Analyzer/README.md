# 📄 Research Paper Analyzer using LLM

An AI-powered **Research Paper Analyzer** built with **LangChain**, **Mistral AI**, and **Python**. Upload a research paper in PDF format, and the application analyzes it to generate summaries, explain concepts in simple language, identify key contributions, and answer questions based solely on the paper.

---

## 🚀 Features

* 📑 Load research papers from PDF
* ✂️ Automatically split large documents into chunks
* 🤖 Analyze papers using Mistral AI
* 📝 Generate a structured summary (200–300 words)
* 💡 Explain research papers in beginner-friendly language
* 🎯 Identify the research problem
* ✅ Describe the proposed solution
* 🌟 Highlight key contributions
* 📌 Extract important points
* 📖 Answer user questions using only the research paper
* 💬 Interactive terminal chatbot

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
Research Paper (PDF)
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
Research Paper Analysis
```

---

## 📁 Project Structure

```text
ResearchPaper/
│
├── research_paper.pdf
├─  main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone <repository-url>

cd ResearchPaper

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

* Summarize this research paper.
* Explain the paper in simple language.
* What problem does this paper solve?
* What is the proposed solution?
* List the key contributions.
* Generate important points.
* Explain the methodology.
* What is the final conclusion?
* What are the limitations?
* What future work is suggested?

---

## 📚 Learning Concepts

* Large Language Models (LLMs)
* Prompt Engineering
* Document Loading
* Text Chunking
* ChatPromptTemplate
* PDF Processing
* LangChain Pipelines

---

## 🔮 Future Improvements

* Multi-PDF support
* Research paper comparison
* Citation extraction
* Keyword extraction
* Streamlit Web App
* Retrieval-Augmented Generation (RAG)
* Vector Database Integration

---

## ⭐ Author

**Bashudev Bhusal**

Built while learning **Generative AI, LangChain, and Large Language Models (LLMs)**.
