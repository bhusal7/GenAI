# AI News Summarizer 🤖📰

A simple Python script that fetches the latest AI news using **Tavily Search** and summarizes it into clear bullet points using **Mistral AI** (via LangChain).

## How It Works

1. **Search** — Uses `TavilySearchResults` to search the web for the latest AI news.
2. **Summarize** — Feeds the search results into a `ChatMistralAI` LLM through a LangChain prompt template.
3. **Output** — Prints a clean, bullet-point summary of the news, along with metadata about the search tool used.

## Requirements

- Python 3.9+
- API Keys:
  - [Mistral AI API Key](https://console.mistral.ai/)
  - [Tavily API Key](https://tavily.com/)

## Installation

1. Clone this repository or copy the script into a project folder.

2. Install the required dependencies:

   ```bash
   pip install python-dotenv langchain-community langchain-mistralai langchain-core tavily-python
   ```

3. Create a `.env` file in the project root with your API keys:

   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## Usage

Run the script directly:

```bash
python main.py
```

By default, it searches for **"Latest AI News of 2026"** and prints:

- A bullet-point summary of the news
- The search tool's name, description, and expected arguments

## Example Output

```
- Company X released a new multimodal model with improved reasoning...
- Regulators in Y region proposed new AI governance guidelines...
- Researchers announced a breakthrough in efficient model training...

Name: tavily_search_results_json
Description: A search engine optimized for comprehensive, accurate, and trusted results...
Query: {'query': {'title': 'Query', 'type': 'string'}}
```

## Customization

- **Change the search topic**: Edit the string passed to `search_tool.run(...)`.
- **Adjust creativity**: Modify the `temperature` parameter in `ChatMistralAI`.
- **Change the prompt**: Edit the `ChatPromptTemplate` to customize the summary style or format.

## Project Structure

```
.
├── main.py        # Main script
├── .env            # API keys (not committed to version control)
└── README.md       # Project documentation
```

## Notes

- Make sure your `.env` file is added to `.gitignore` to avoid leaking API keys.
- `TavilySearchResults` returns raw search snippets; the LLM summarizes them into readable bullet points.

## License

This project is open-source and available for personal or educational use.
