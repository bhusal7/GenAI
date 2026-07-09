from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class Recipe(BaseModel):
    recipe_name:str
    ingredients:List[str]
    cooking_time:str
    difficulty:Optional[str]
    steps:List[str]
    
parser = PydanticOutputParser(pydantic_object=Recipe)

print("Recipe Information Extractor")
print("Press 1 for Vegetarian")
print("Press 2 for Non-Vegetarian")
print("Press 3 for Dessert")

choice = input("Enter your Choice :- ")
if choice == '1':
    mode = "Vegetarian Recipe"
elif choice == '2':
    mode = "Non-Vegetarian Recipe"
elif choice == '3':
    mode = "Dessert Recipe"
else:
    print("Invalid Choice!")
    exit()

prompt = ChatPromptTemplate([
    ("system","""
You are an expert recipe information extractor.

The recipe belongs to the following category:
{mode}
Extract the following information:
- Recipe Name
- Ingredients
- Cooking Time
- Difficulty (if available)
- Preparation Steps
Return the output in the required format.
{format_instructions}
     """),
    ("human","{recipe}")
])

messages = [
    SystemMessage(content=mode)
]

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.9
    )

chain = prompt|model

while True:
    recipe_text = input("Enter the Recipe :- ")
    if recipe_text == '0':
        break
    messages.append(HumanMessage(content=recipe_text ))

    response = chain.invoke({
        'recipe':recipe_text,
        'mode':mode,
        "format_instructions":parser.get_format_instructions()
    })
    messages.append(AIMessage(content=response.content))
try:
    parse_response = parser.parse(response.content)
    print(parse_response)
except Exception:
    print(response.content)
    
print("\nConversation History\n")
for msg in messages:
    print(f"{msg.type.upper()} : {msg.content}")