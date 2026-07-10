from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv() 

data = PyPDFLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/RAG/documents_loader/deeplearning.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

templete = ChatPromptTemplate.from_messages([
    ('system', 
     "you're a AI that summarize the text"
     ),
    ('human', "{data}")
])

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.9
    )

prompt = templete.format_messages(data = docs)

result = model.invoke(prompt)
print(result.content)