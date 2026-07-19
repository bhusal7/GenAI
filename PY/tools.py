from langchain.tools import tool
import os
from functools import lru_cache
import requests
from rich import print
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@lru_cache(maxsize = 32)
def cache_web_search(query:str):
    """Search the web for recent and reliable information an a topic. Returns Titles, URLs , Snippets"""
    results = tavily_client.search(query=query,max_results=5)
    
    return results


@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information."""
    response = cache_web_search(query)
    if not response:
        return "No result found"
    
    output = []
    for r in response['results']:
        output.append(
            f"Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}"
            )
        
    return "\n--------\n".join(output)

# Beautiful Soap 
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
print(scrape_url.invoke("https://www.bbc.com/news/topics/cx2jyv8j8gwt"))


        
    