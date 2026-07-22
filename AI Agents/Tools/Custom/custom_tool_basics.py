#   Use Case of Custom Tool
from langchain.tools import tool

@tool
def get_greeting(name : str) -> str:
    """Generate a greeting message for a user"""
    return f"Hello {name}, Welcome to the AI world "
# aba yo tool hamro yo function ko mathi "Decorater" bancha

result = get_greeting.invoke({
    "name":"Bashudev"
})
print(result)

print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args)