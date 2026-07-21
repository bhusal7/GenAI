# 📊 CSV Insight Pipeline

An automated, multi-agent CSV analysis tool built with **Streamlit** and **LangChain/LangGraph**-style agents. Upload a CSV file and the pipeline will run it through a sequence of agents to produce exploratory data analysis, visualizations, correlation analysis, a written report, and critic feedback — all from a simple web UI.

## ✨ Features

- **📁 Simple upload flow** — drag and drop a CSV file from the sidebar
- **🤖 Multi-agent pipeline** — five stages run in sequence, each with live status updates:
  1. **EDA Agent** — exploratory data analysis of the uploaded CSV
  2. **Visualization Agent** — generates charts/plots from the data
  3. **Correlation Agent** — analyzes relationships between variables
  4. **Writer Chain** — synthesizes agent outputs into a written report
  5. **Critic Chain** — reviews the report and provides feedback
- **📈 Tabbed results view** — Report, Critic Feedback, EDA, Visualization, and Correlation results each in their own tab
- **🖼 Plot gallery** — automatically displays any generated plots from the `plots/` folder
- **⬇️ Downloadable report** — export the final report as a `.txt` file
- **📱 Responsive UI** — clean, mobile-friendly layout with custom styling

## 🗂 Project Structure

```
.
├── app.py              # Streamlit application (entry point)
├── PY/
│   └── agents.py        # Agent and chain builders (EDA, visualization, correlation, writer, critic)
├── plots/               # Generated visualization plots (created at runtime)
└── README.md
```

## 🔧 Requirements

- Python 3.9+
- [Streamlit](https://streamlit.io/)
- LangChain / LangGraph (or equivalent agent framework used in `PY/agents.py`)
- Any additional dependencies required by your agent implementations (e.g. `pandas`, `matplotlib`, an LLM provider SDK, API keys, etc.)

Install dependencies, for example:

```bash
pip install -r requirements.txt
```

> **Note:** This repo assumes a `PY/agents.py` module that exports `build_eda_agent`, `build_visualization_agent`, `build_correlation_agent`, `writer_chain`, and `critic_chain`. Make sure this module (and any API keys/environment variables it needs, such as an LLM provider key) is configured before running the app.

## 🚀 Usage

1. Clone the repository and install dependencies.
2. Set any required environment variables (e.g. LLM API keys) that `PY/agents.py` depends on.
3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Open the app in your browser (Streamlit will print a local URL, typically `http://localhost:8501`).
5. Upload a CSV file using the sidebar uploader.
6. Click **▶ Run Pipeline** to execute all five agent stages.
7. Explore the results across the tabs, and use **Download report (.txt)** to save the final report.
8. Click **🗑 Clear Results** to reset and start over.

## 🧠 How It Works

When you click **Run Pipeline**, the uploaded CSV is temporarily saved to disk and passed through each agent/chain in order. Progress is streamed live to the UI via `st.status`, and each stage's output is stored in session state:

| Stage | Input | Output Key |
|---|---|---|
| EDA Agent | CSV file path | `eda_results` |
| Visualization Agent | CSV file path | `viz_results` |
| Correlation Agent | CSV file path | `cor_results` |
| Writer Chain | Truncated EDA/Viz/Correlation results | `report` |
| Critic Chain | Truncated report | `feedback` |

The temporary CSV file is deleted after the pipeline completes (or fails)`, and results persist in the Streamlit session until cleared or the app is restarted.

## 📌 Notes

- Visualization plots are expected to be saved by the Visualization Agent into a local `plots/` directory as `.png` files; the app automatically discovers and displays them.
- Each stage's output passed to downstream chains is truncated (2,000–3,000 characters) to keep prompts within reasonable limits.
- If the pipeline fails at any step, an error message is shown and the app resets to a ready state.

## 📄 License

Add your project's license here (e.g. MIT, Apache 2.0).