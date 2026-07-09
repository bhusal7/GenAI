from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class Resume(BaseModel):
    name:str
    email:str
    education:Optional[str]
    experience:Optional[str]
    skills:List[str]
    company:Optional[str]
    
parser = PydanticOutputParser(pydantic_object=Resume)

print("========== Resume Type ==========")
print("1. Basic Resume")
print("2. Fresher Resume")
print("3. Experienced Resume")

choice = input("Enter your choice: ")

if choice == "1":
    mode = "The resume belongs to a basic candidate."
elif choice == "2":
    mode = "The resume belongs to a fresher candidate."
elif choice == "3":
    mode = "The resume belongs to an experienced candidate."
else:
    print("Invalid Choice!")
    exit()
    
prompt = ChatPromptTemplate([
    ("system","""
You are an expert Resume Information Extractor.
{mode}   
     
Extract student information from the Resume
    {format_instructions}  
"""), 
    ("human","{resume}")
])

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.9
    )

chain = prompt | model

messages = [
    SystemMessage(content=mode)
]


print("------------------- Welcome type 0 to exit the application-----------------------------")
while True:
    resume_text = input("Give your resume:- ")
    if resume_text == "0":
        break

    messages.append(HumanMessage(content=resume_text))
    
    response = chain.invoke(
        {
            "resume" : resume_text,
            "mode":mode,
            "format_instructions": parser.get_format_instructions()
            }
        )
    messages.append(AIMessage(content=response.content))
    
try:
    parse_respond = parser.parse(response.content)
    print(parse_respond)
except Exception:
    print(response.content)

print("Messages History : ", messages)