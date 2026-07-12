# ----------- LLM APPLICATION -----------------

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

data = PyPDFLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/Projects/Smart Notes Generator/pythonlearn.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap = 70
)

chunks = splitter.split_documents(docs)

notes = "\n\n".join(chunk.page_content for chunk in chunks)

text_history = []

templete = ChatPromptTemplate([
    (
    "system",
    """
    You are an intelligent Smart Notes Generator.

    Your task is to analyze the provided document and answer the user's request.

    Rules:
    - Use ONLY the information from the document.
    - Generate clear and structured notes.
    - Use headings and bullet points whenever appropriate.
    - Keep explanations concise but informative.
    - If the information is not present in the document, politely say so.
    - Never make up facts.
    """
),
    (
    "human",
    """
    Here is the document:

    {notes}

    User Request:
    {question}
    """
)
])

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
)

print("------------ Smart Notes Generator ChatBox---------------\n")
print("********* Print 'exit' to Quit the App ******************\n")

while True:
    question = input("You : ")
    if question.lower() == 'exit':
        break
    prompt = templete.format_messages(
        notes= notes,
        question = question
    )
    
    response = model.invoke(prompt)
    
    print("Bot : ", response.content)
    
    text_history.append(('You : ',question))
    text_history.append(('Bot : ',response.content))\
        
for roles, history in text_history:
    print(f"{roles}:{history}")
