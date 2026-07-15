import os
from langchain.tools import tool
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_market_news(topic: str) -> str:
    """Get the latest financial/market news about a stock, company, or topic."""
    response = tavily_client.search(
        query=f"latest financial news about {topic}",
        search_depth="basic",
        max_results=3,
    )

    results = response.get("results", [])
    if not results:
        return f"No news found for {topic}"

    news_list = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")
        news_list.append(f"- {title}\n  Link: {url}\n  Summary: {snippet[:120]}...")

    return f"Latest news on {topic}:\n\n" + "\n\n".join(news_list)
