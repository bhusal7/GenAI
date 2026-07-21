# 🧠 Deep Research Agent

A Streamlit-based research assistant powered by [LangChain](https://www.langchain.com/) and [Mistral AI](https://mistral.ai/), featuring a **human-in-the-loop (HITL) approval flow** for every tool call the agent makes. Instead of blindly executing tool calls, the agent pauses and waits for the user to click **Approve** or **Deny** directly in the UI before proceeding.

## ✨ Features

- **Conversational research agent** built with `langchain.agents.create_agent`
- **Human-in-the-loop tool approval** — review and approve/deny each tool call (stock price lookups, market news, etc.) before it executes
- **Auto-approve toggle** for faster iteration when review isn't needed
- **Live tool call log** in the sidebar showing what was called, with what arguments, and the decision made
- **Background-threaded agent execution** so the Streamlit UI stays responsive while the agent works
- **Environment variable status check** in the sidebar to confirm required API keys are set

## 🏗️ How It Works

Streamlit apps can't block on a plain `input()` call for human approval, so this app runs the agent in a **background thread** and uses a shared `AgentBridge` object plus a `threading.Event` to pause the agent thread until the user responds via the UI. A `@st.fragment(run_every=0.5)` polling loop checks for:

- A pending tool call awaiting approval → renders Approve/Deny buttons
- An agent still running → shows a spinner
- A finished result or error → appends it to the chat history

## 📦 Requirements

- Python 3.9+
- API keys for:
  - `MISTRAL_API_KEY` — Mistral AI (LLM)
  - `ALPHAVANTAGE_API_KEY` — stock price data
  - `TAVILY_API_KEY` — market news / search

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key
   ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   Replace `app.py` with the actual filename of this script if different.

## 🖥️ Usage

- Type a research question or topic in the chat box.
- Type `report: <topic>` to generate a full markdown research report.
- When the agent wants to call a tool (e.g., fetch a stock price or market news), you'll see an approval prompt — click **✅ Approve** or **❌ Deny**.
- Toggle **Auto-approve tool calls** in the sidebar to skip manual approval.
- Use **Clear conversation** in the sidebar to reset the chat and tool log.

## 📁 Expected Project Structure

```
.
├── app.py                  # Main Streamlit app (this file)
├── tools/
│   ├── stock_tool.py        # get_stock_price tool
│   └── news_tool.py         # get_market_news tool
├── requirements.txt
├── .env                     # Not committed — holds API keys
└── README.md
```

## ⚠️ Warnings & Notes

- **Never commit your `.env` file or API keys** to GitHub. Add `.env` to your `.gitignore` before pushing.
- This app calls external APIs (Mistral, Alpha Vantage, Tavily) — usage may incur costs or be subject to rate limits depending on your plan with each provider.
- The human-in-the-loop approval step is a **safety/review mechanism**, not a security sandbox — approved tool calls still execute with whatever permissions the tool code has.
- `@st.cache_resource` is used for the LLM and agent instances; if you change model config or agent setup during development, you may need to clear Streamlit's cache or restart the app to see changes take effect.
- The background thread approach relies on Streamlit's `st.fragment` polling (every 0.5s) — very long-running tool calls will still work, but the UI will only refresh at that interval.

## 📄 License

Add your preferred license here (e.g., MIT) before publishing to GitHub.
