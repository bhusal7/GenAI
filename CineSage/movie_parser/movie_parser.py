from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

# for schema - 
from pydantic import BaseModel
from typing import List, Optional

# for Parsers -
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-large-latest", temperature=0.9)


# creating schema
class Movie(BaseModel):
   title : str
   release_year : Optional[int]
   genre : List[str]
   director : Optional[str]
   cast : List[str]
   rating : Optional[float]
   summary : str


# creating parsers
parser = PydanticOutputParser(pydantic_object=Movie)


prompt = ChatPromptTemplate.from_messages([
   ('system',"""
Extract movie information from the paragraph
    {format_instructions}
"""),
   ("human","{paragraph}")
]
)


paragraph = input("Give your paragraph : ")

chain = prompt | model

 
response = chain.invoke(
    {"paragraph": paragraph,
     'format_instructions' : parser.get_format_instructions()
     }
)

print(response.content)
