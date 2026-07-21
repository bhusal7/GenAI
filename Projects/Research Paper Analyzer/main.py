# ----------- LLM APPLICATION -----------------

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

data = PyPDFLoader("Projects/ResearchPaper/research_paper.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_documents(docs)

templete = ChatPromptTemplate([
    ("system",
"""
You are an expert research paper analyzer.

Your job is to carefully read the provided research paper and produce a structured response.

Follow these rules:
1. Summarize the paper in 200-300 words.
2. Explain the paper in simple language suitable for a beginner.
3. List the most important points.
4. Mention the problem the paper solves.
5. Describe the proposed solution.
6. Mention the key contributions.
7. Provide the final conclusion.

Only use information present in the paper.
Do not invent facts.
Use clear headings and bullet points.
"""
),
    ("human",
"""
Research Paper:

{paper}

Question:
{question}
"""
)
])

messages = []

paper = '\n\n'.join(chunk.page_content for chunk in chunks)

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
)

print("------------ Research Paper ChatBox---------------\n")
print("********* Print 'exit' to Quit the App ******************\n")

while True:
    question = input("You : \n")
    if question.lower() == 'exit':
        break
    
    prompt = templete.format_messages(
        paper = paper,
        question = question
        )
    
    response = model.invoke(prompt)
    
    print("\nBot :", response.content)
    
    messages.append(("You :",question))
    messages.append(("Bot :",response.content))
    
    
print("******Messages History***********")
for role, message in messages:
    print(f"{role}:{message}")