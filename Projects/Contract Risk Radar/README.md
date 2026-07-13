# ⚖️ Enterprise Legal Contract Risk Analyzer (RAG)

An AI-powered Legal Contract Risk Analyzer built using Retrieval-Augmented Generation (RAG), LangChain, Mistral AI, ChromaDB, and HuggingFace Embeddings.

The application analyzes legal contracts from PDF files or web pages, identifies risky clauses, assigns risk levels, and provides structured recommendations for legal review.

---

# Features

- AI-powered Legal Contract Analysis
- PDF Contract Analysis
- Website Contract Analysis
- MultiQueryRetriever for better document retrieval
- Chroma Vector Database
- HuggingFace Embeddings
- Mistral Large Language Model
- Structured JSON Output using Pydantic
- Interactive Streamlit Web Interface
- Command Line Interface (CLI)
- Risk Classification
- Clause-by-Clause Analysis
- Chat History
- General Legal Assistant (without document)

---

# Tech Stack

## Language

- Python

## LLM

- Mistral Large

## Framework

- LangChain

## Vector Database

- ChromaDB

## Embedding Model

- sentence-transformers/all-MiniLM-L6-v2

## Retrieval

- MultiQueryRetriever

## Frontend

- Streamlit

## Validation

- Pydantic

---

# Project Structure

```
Legal-Contract-Risk-Analyzer-RAG/
│
├── app.py                 # Streamlit Web Application
├── main.py                # Command Line Version
├── requirements.txt
├── .env
├── README.md
├── Rag_Project.pdf
├── chroma_db/
└── assets/
```

---

# How It Works

```
Contract (PDF / URL)
          │
          ▼
Document Loader
          │
          ▼
Token Text Splitter
          │
          ▼
Embedding Model
(HuggingFace)
          │
          ▼
Chroma Vector Database
          │
          ▼
MultiQuery Retriever
          │
          ▼
Mistral LLM
          │
          ▼
Risk Analysis
          │
          ▼
Structured JSON Report
```

---

# Risk Categories

The application identifies risks related to:

- Liability
- Indemnification
- Confidentiality
- Intellectual Property
- Termination
- Auto Renewal
- Non-Compete
- Payment Obligations
- Penalties
- Warranties
- Arbitration
- Governing Law

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Legal-Contract-Risk-Analyzer-RAG.git
```

Move into the project

```bash
cd Legal-Contract-Risk-Analyzer-RAG
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
MISTRAL_API_KEY=your_api_key
```

---

# Running the CLI Version

```bash
python main.py
```

The CLI allows users to:

- Load contract documents
- Ask legal questions
- View structured risk reports
- Review chat history

---

# Running the Streamlit App

```bash
streamlit run app.py
```

The Streamlit interface supports:

- Upload Contract PDF
- Analyze Contract Website
- Chat with AI
- General Legal Questions
- Structured Risk Reports

---

# Sample Output

```
Contract Name:
Employment Agreement

Overall Risk:
HIGH

Clause 1
Risk:
CRITICAL

Reason:
Unlimited liability clause may expose one party to significant financial risk.

Recommendation:
Review and negotiate the liability and indemnification clauses before signing.
```

---

# Core Components

### Document Loading

- PyPDFLoader
- WebBaseLoader

### Text Processing

- TokenTextSplitter

### Embeddings

- HuggingFace Embeddings
- all-MiniLM-L6-v2

### Vector Store

- ChromaDB

### Retrieval

- MultiQueryRetriever

### Language Model

- Mistral Large

### Output Parsing

- PydanticOutputParser

---

# Future Improvements

- OCR Support
- DOCX Contract Analysis
- Multiple Contract Comparison
- Contract Summarization
- Risk Score Dashboard
- Highlight Risky Clauses in PDF
- Export PDF Reports
- User Authentication
- Conversation Memory
- Multi-language Support

---

# Author

**Bashudev Bhusal**

AI | Machine Learning | Generative AI Developer

---

# License

This project is developed for educational and portfolio purposes.