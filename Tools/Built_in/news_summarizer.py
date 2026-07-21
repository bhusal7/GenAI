#   Use Case of Built-in Tools
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import  StrOutputParser

load_dotenv()

search_tool =  TavilySearchResults(max_result = 5)

llm = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
    )

prompt = ChatPromptTemplate.from_template(
    """
You're a helpful assistant

summarize the following news into clear bullet points
{news}
    """
)

chain = prompt | llm | StrOutputParser()

news_result = search_tool.run("Latest AI News of 2026")
# yo news_result mathi {news} ma jancha, haita la

result = chain.invoke({"news":news_result})

print(result)

print("Name:",search_tool.name)
print("Description:",search_tool.description)
print("Query:",search_tool.args)

