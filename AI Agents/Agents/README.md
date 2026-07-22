# 🌍 City Intelligence System Agent

An AI-powered **City Intelligence System** built with **LangChain Agents**, **Mistral AI**, **OpenWeather API**, and **Tavily Search API**. This intelligent agent can answer city-related questions by automatically selecting and calling the appropriate tools to fetch **live weather** and **latest news**.

The project demonstrates how to build a real-world AI Agent using LangChain's `create_agent()` with **Human-in-the-Loop (HITL)** approval before every tool execution.

---

## 🚀 Features

- 🌦️ Get real-time weather of any city
- 📰 Fetch the latest news related to a city
- 🤖 AI Agent powered by Mistral Large
- 🔧 Automatic Tool Selection
- 👨‍💻 Human-in-the-Loop (Approval before every tool call)
- 🧠 LangChain `create_agent()`
- ⚡ Middleware using `wrap_tool_call`
- 💬 Interactive command-line chat interface
- 🔄 Multi-turn conversations

---

# 🛠️ Tech Stack

- Python
- LangChain
- LangChain Agents
- Mistral AI
- Tavily Search API
- OpenWeather API
- Requests
- python-dotenv
- Rich

---

# 📂 Project Structure

```text
City-Intelligence-System/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/City-Intelligence-System.git
```

Move into the project

```bash
cd City-Intelligence-System
```

Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

```bash
python app.py
```

---

# 💬 Example

```
City Agent

Type 'exit' to quit

You : What's the weather in Delhi?

Agent wants to call 'get_weather'. Approve? (yes/no)

yes

Bot :
The current weather in Delhi is cloudy with a temperature of 31°C.
```

---

# 🧠 Agent Workflow

```
User
   │
   ▼
ChatMistralAI
   │
   ▼
create_agent()
   │
   ▼
Tool Selection
   │
   ▼
Human Approval
   │
   ▼
Weather Tool / News Tool
   │
   ▼
API Response
   │
   ▼
LLM Generates Final Answer
   │
   ▼
User
```

---

# 🔄 Complete Pipeline

```text
User Question
      │
      ▼
ChatMistralAI
      │
      ▼
LangChain create_agent()
      │
      ▼
Reasoning
      │
      ▼
Does the Agent Need a Tool?
      │
      ├───────────────No────────────────► Generate Response
      │
      ▼
Choose Tool
      │
      ▼
Human Approval Middleware
      │
      ├────────Denied────────► Return "Tool Call Denied"
      │
      ▼ Approved
Execute Tool
      │
      ├───────────────┐
      │               │
      ▼               ▼
Weather Tool      News Tool
      │               │
      ▼               ▼
OpenWeather API   Tavily API
      │               │
      └──────┬────────┘
             ▼
      Tool Output
             │
             ▼
ChatMistralAI
             │
             ▼
Final Response
             │
             ▼
User
```

---

# 🔧 Tools

## 🌦️ Weather Tool

Uses **OpenWeather API** to fetch:

- Current Temperature
- Weather Condition
- City Weather Information

---

## 📰 News Tool

Uses **Tavily Search API** to fetch:

- Latest News
- Top Headlines
- Relevant News Links
- News Summary

---

# 🤖 Agent Components

- ChatMistralAI
- create_agent()
- Tool Binding
- Tool Calling
- Tool Execution
- Middleware
- Human Approval
- Conversation Memory

---

# 📚 Concepts Covered

- LangChain Agents
- Custom Tools
- Tool Calling
- Tool Execution
- Middleware
- Human-in-the-Loop
- API Integration
- Prompt Engineering
- Environment Variables
- Multi-turn Conversations

---

# 📦 Dependencies

```text
langchain
langchain-mistralai
langchain-core
python-dotenv
requests
tavily-python
rich
```

---

# 📄 Main File

```
app.py
```

---

# 👨‍💻 Author

**Bashudev Bhusal**

Passionate about AI, Machine Learning, Deep Learning, Generative AI, and Building Intelligent AI Agents.

GitHub:
https://github.com/bhusal7

---

# ⭐ If you like this project

Give the repository a ⭐ on GitHub and feel free to fork it to build your own intelligent AI agents.

---

## 📜 License

This project is developed for educational and learning purposes.