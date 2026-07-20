# Multi-Agent Research System

A small multi-agent research pipeline with a Streamlit UI.

Given a topic, four components run in sequence:

1. **Search Agent** (`agents.py`) – uses the `web_search` tool (Tavily) to find recent, relevant sources.
2. **Reader Agent** (`agents.py`) – uses the `scrape_url` tool (requests + BeautifulSoup) to pull deeper content from the most relevant page.
3. **Writer Chain** (`agents.py`) – a Mistral LLM chain that drafts a structured markdown report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** (`agents.py`) – a second LLM pass that scores and critiques the report.

`pipeline.py` wires these four steps together, and `app.py` exposes them through a Streamlit UI.

## Project structure

```
Multi Agent System/
├── app.py              # Streamlit UI (new)
├── pipeline.py          # Orchestrates the 4-step pipeline
├── agents.py             # Defines the agents + writer/critic chains
├── tool.py               # web_search, scrape_url, save_report tools
├── requirements.txt      # Python dependencies (new)
├── .env.example           # Template for API keys (new)
└── README.md              # This file (new)
```

## Fixes made while wiring up the UI

Two bugs in the original code would have crashed the app, so they were corrected:

- **`agents.py`** imported `from tools import web_search, scrape_url`, but the file is named `tool.py` (singular). Changed the import to `from tool import web_search, scrape_url`.
- **`tool.py`** had a module-level call `print(scrape_url.invoke("https://www.bbc.com/..."))`. This ran a live network scrape every single time the module was imported (including every Streamlit rerun), which is slow, noisy, and unnecessary. It has been removed. The `rich` import (only used for that line) was removed too — everything else is unchanged.

Nothing about the pipeline's logic was altered. `pipeline.py` got one small, backward-compatible addition: an optional `progress_callback` parameter so the UI can show live step-by-step status. If you call `run_research_pipeline(topic)` without it (e.g. from the CLI, as `if __name__ == "__main__"` still does), behavior is identical to before.

## Setup

1. **Install dependencies**

   ```bash
   cd "Multi Agent System"
   pip install -r requirements.txt
   ```

2. **Add API keys**

   Copy `.env.example` to `.env` and fill in your keys:

   ```bash
   cp .env.example .env
   ```

   ```
   TAVILY_API_KEY=your_tavily_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   - Get a Tavily key at https://tavily.com
   - Get a Mistral key at https://console.mistral.ai

## Running the app

```bash
streamlit run app.py
```

This opens the UI in your browser (default: http://localhost:8501).

### Using it

1. Check the sidebar — it shows whether your API keys were detected.
2. Type a research topic into the input box.
3. Click **🚀 Run Research**. A live status panel shows each agent step as it runs (search → read → write → critique).
4. When it finishes, results are shown in four tabs:
   - **📄 Final Report** – the finished markdown report, downloadable as a `.md` file, or savable to the server's `reports/` folder (via the existing `save_report` tool).
   - **🧐 Critic Feedback** – the critic's score, strengths, and areas to improve.
   - **🔍 Search Results** – raw output from the search agent.
   - **📰 Scraped Content** – raw scraped text from the reader agent.
5. **🗑️ Clear results** resets the page for a new topic.

## Running from the command line (unchanged)

The original CLI entry point still works:

```bash
python pipeline.py
```

## Notes

- `web_search` results are cached in-process (`lru_cache`) per query string, so re-running the exact same topic within the same session won't re-hit the Tavily API.
- `scrape_url` truncates page text to 3,000 characters to keep prompts a reasonable size.
- Reports saved via **Save report to disk** are written to a `reports/` folder created alongside wherever the Streamlit process is run from, with a timestamp appended to the filename.
- If a step fails (e.g. bad API key, network error), the Streamlit status panel turns red and the error message is shown — the app won't crash, you can just fix the issue and click **Run Research** again.
