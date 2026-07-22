from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from rich import print
load_dotenv()

# creating a tool
@tool
def get_text_length(text : str) -> int:
    """Returns the number of characters in a given text"""
    # Dogstring - yesle hamro LLM lai tool ko usecare bare bataucha so lekhnai parcha
    
    return len(text)

tools = {
    "get_text_length" : get_text_length
}

llm = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
    )

# Tool Binding
  # - In this , we gave tools to LLM   
llm_with_tool = llm.bind_tools([get_text_length])
# the purpose of binding i.e it connects our tools to the LLM so it can use them when needed
# we give our tools to LLM & now the LLM follows:
#    1. what tools are available
#    2. what they do
#    3. when to use them  - for this no. 3 we do Tool Calling below :-


# Tool Calling
  # - In this , LLM choose to use them
  
# Tool Execution
     # Tool execution is when we actually run the tool after the LLM decides to use it.
     # LLM selects the tool → we execute it → get the result → send it back to LLM.

messages = []
prompt = input("You :")
query = HumanMessage(prompt)
messages.append(query)

result = llm_with_tool.invoke(messages)
messages.append(result)
# print(messages)   # - it's AI Message

if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_message = tools[tool_name].invoke(result.tool_calls[0])
    messages.append(tool_message)   # - it's Tool Message
    
    # print(messages)  - it prints ther final msg include: human, AI & Tool Messages
    
response = llm_with_tool.invoke(messages)
print(response.content)
     