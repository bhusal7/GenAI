# 🤖 AI Code Assistant

An intelligent **Multi-Agent AI Code Assistant** powered by **RAG (Retrieval-Augmented Generation)**, **LangChain**, **Mistral AI**, **ChromaDB**, and **Streamlit**.

The assistant analyzes source code, retrieves relevant project context, detects bugs, suggests optimizations, generates documentation, explains code, critiques its own report, and automatically saves the final analysis.

---

# 🚀 Features

* 🔍 Retrieval-Augmented Generation (RAG)
* 🤖 Multi-Agent Architecture
* 🐞 Bug Detection
* ⚡ Code Optimization Suggestions
* 📖 Automatic Documentation Generation
* 💡 Code Explanation
* 📝 AI Report Generation
* 🎯 Critic Agent for Self-Review
* 💾 Automatic Report Saving
* 🌐 Interactive Streamlit Web Interface

---

# 🏗️ Project Architecture

```text
                 User Query
                      │
                      ▼
             ┌────────────────┐
             │  RAG Retriever │
             └────────────────┘
                      │
                      ▼
            Retrieved Code Context
                      │
                      ▼
        ┌──────────────────────────┐
        │      User Agent          │
        └──────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │    Research Agent        │
        └──────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │      Bug Agent           │
        └──────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │ Optimization Agent       │
        └──────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │ Documentation Agent      │
        └──────────────────────────┘
                      │
                      ▼
             Explain Chain
                      │
                      ▼
              Critic Chain
                      │
                      ▼
              Final AI Report
                      │
                      ▼
                Saved Report
```

---

# 📂 Project Structure

```text
AI_Code_Assistant/
│
├── Agents/
│   └── agents.py
│
├── RAG/
│   ├── document_loader.py
│   ├── indexing.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── Tools/
│   └── tools.py
│
├── data/
│
├── Reports/
│
├── app.py
├── pipeline.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies Used

* Python
* LangChain
* LangGraph
* Mistral AI
* HuggingFace Embeddings
* ChromaDB
* Streamlit
* FAISS (optional)
* Pydantic
* dotenv

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AI_Code_Assistant.git
cd AI_Code_Assistant
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
MISTRAL_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```

---

# ▶️ Run the Streamlit Application

```bash
streamlit run app.py
```

---

# 💬 Example Queries

* Explain authentication.py
* Find bugs in login.py
* Optimize the API layer
* Generate documentation for this project
* Explain how the database module works
* Suggest performance improvements
* Review this codebase

---

# 🔄 Pipeline Workflow

1. User submits a query.
2. RAG retrieves the most relevant code.
3. User Agent interprets the request.
4. Research Agent gathers additional insights.
5. Bug Agent detects issues.
6. Optimization Agent recommends improvements.
7. Documentation Agent generates documentation.
8. Explain Chain creates the consolidated report.
9. Critic Chain reviews the report.
10. Final report is automatically saved.

---

# 📸 Streamlit Dashboard

The dashboard includes:

* Interactive query input
* Retrieved code context
* Individual outputs from every AI agent
* Final AI-generated report
* Critic feedback
* Automatic report generation

---

# 🌟 Future Improvements

* GitHub Repository Analysis
* PDF Report Export
* Code Diff Viewer
* File Upload Support
* Multi-language Code Analysis
* Conversation Memory
* CI/CD Integration
* Docker Support
* Cloud Deployment
* Authentication System

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Bashudev Bhusal**

Passionate about Artificial Intelligence, Machine Learning, and Generative AI.

⭐ If you found this project useful, consider giving it a star on GitHub!
