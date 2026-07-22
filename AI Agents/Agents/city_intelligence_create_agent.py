# city intelligence system

import os
import requests
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

load_dotenv()

# now let's create tool
   #  weather tool
         
@tool
def get_weather(city : str) -> str:
    """Get current weather of a city"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    # print("DEBUG:", data)
    
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    
    return f"Weather in {city}: {desc}, {temp}°C"

print(get_weather.invoke("Bhopal"))

print("==============Weather finished====================")

print("********************************************************************")
print(os.getenv("OPENWEATHER_API_KEY"))
print(os.getenv("TAVILY_API_KEY"))
print("********************************************************************")



#  News Tool (Tavily)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city : str) -> str:
    """Get latest news about a city"""
    
    response = tavily_client.search(
        query = f"latest news in {city}",
        search_depth = "basic",
        max_results = 3
    )
    
    results = response.get("results",[])
    
    if not results:
        return f"No news found for {city}"
    
    news_list = []
    
    for r in results:
        title = r.get("title","NO title")
        url = r.get("url","")
        snippet = r.get("content","")
        
        news_list.append(
            f"- {title}\n  🔗 {url}\n  📝 {snippet[:100]}..."
            )
    
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

print(get_news.invoke("Bhopal"))


# 🧠 LLM Setup

llm = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
    )

# Human in the loop
@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call."""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'. Approve? (yes/no): ")

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request) 

# request - Sabai AI msg huncha hiata la 

agent = create_agent(
    llm,
    tools = [get_weather, get_news],
    system_prompt = "you are a helpful city assistance",
    middleware=[human_approval]
)

print("City Agent")
print("Type 'exit' to quit")

while True:
    
    user_input = input("You :")
    if user_input.lower() == "exit":
        break
    result = agent.invoke({
        "messages" : [{"role":"user","content":user_input}]
    })
    print("Bot :",result['messages'][-1].content)
    # -1 kina garya vanda AI msg last ma aucha so last ko select grna PY. ma -1 grna parcha- basis
    


