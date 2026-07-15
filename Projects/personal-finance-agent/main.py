import os
import requests
from dotenv import load_dotenv

load_dotenv()
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from tools.stock_tool import get_stock_price
from tools.news_tool import get_market_news

#         `stock_tool.py`
@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol (e.g. AAPL, TSLA)."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    quote = data.get("Global Quote", {})
    if not quote:
        return f"Error: Could not fetch price for {symbol}"

    price = quote.get("05. price", "N/A")
    change = quote.get("10. change percent", "N/A")

    return f"{symbol}: ${price} ({change} change today)"


#            `news_tool.py`
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

# 🧠 LLM Setup

llm = ChatMistralAI(
    model = "mistral-large-latest",
    temperature = 0.2
)

# human-in-the-loop (HITL)
@wrap_tool_call
def human_approval(request,handler):
    """Ask for human approval before every tool call."""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'. Approve? (yes/no): ")
    
    if confirm.lower() != "yes":
        return ToolMessage(
            content = "Tool call denied by user.",
            tool_call_id = request.tool_call['id']
        )
        
    return handler(request)


# creating agent 
agent = create_agent(
    llm,
    tools = [get_stock_price,get_market_news],
    system_prompt = "You are a deep research assistant. When the user gives a topic, "
        "use the search_topic tool (call it 2-3 times with different angles "
        "of the topic if needed) to gather information, then write a clear "
        "summary with sources. If the user asks to save it, use save_report.",
        middleware = [human_approval]
)

print("Deep Research Agent")
print("Type 'exit' to quit")
print("Type 'report: <topic>' to generate a full markdown research report\n")

while True:
    query = input("You : ")
    if query.lower() == "exit":
        break
    
    result = agent.invoke({
        "messages": [{"role":"user", "content":query}]
    })
    
    print("Bot :",result['messages'][-1].content)
