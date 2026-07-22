# City intelligence system 

import os
import requests
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print

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

tools = {
    "get_weather" : get_weather,
    "get_news" : get_news
}
 
llm_with_tool = llm.bind_tools([
    get_weather,
    get_news
])

# Agent Loop - Very Imp
messages = []

print("City Intelligence System")
print("Type 'exit' to quit")

while True:
    user_input = input("You : ")
    if user_input.lower() == "exit":
        break
    messages.append(HumanMessage(content=user_input))
    
    while True:
        result = llm_with_tool.invoke(messages)
        
        messages.append(result)   # = AI input
        if not result.tool_calls:
            print(result.content)
            break
        
        # if tool is required
        
        if result.tool_calls:
            for tool_call in result.tool_calls:
                tool_name = tool_call['name']  # 1st tool call : we extract name
                
                # Human In The Loop
                confirm = input(f"Agent wants to call {tool_name} Approved (yes/no)")
            
                if confirm.lower() == "no":
                    print("Tool Call defined & I can not get the latest information")
                    break
            
            # execute the tool
                tool_result = tools[tool_name].invoke(tool_call["args"])
            
            
                messages.append(ToolMessage(
                content=tool_result,
                tool_call_id = tool_call['id']
            ))
                
    continue
    
else:
    print(result.content)