from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    persist_directory=r"chroma_db",
    embedding_function=embedding_model
)
print("Documents in DB:", vector_store._collection.count())

retriever = vector_store.as_retriever(
    search_type = 'mmr',
    search_kwargs = {
        'k': 3,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)

llm_model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
)

template = ChatPromptTemplate([
   ("system",
"""
You are an AI assistant for answering company policy questions.

Answer only from the provided context.

If the answer is not present in the context, reply:
'I don't know based on the provided company policy.'
"""),
    ("human",
     "Question: {question}\n\nContext:\n{context}")
])

messages = []

print("------------ Company_Policy_Assistant_about_AIML ---------------\n")
print("********* Print 'exit' to Quit the App ******************\n")

while True:
    question = input("You : ")
    if question.lower() == "exit":
        break
    
    docs = retriever.invoke(question)
    print("Retrieved docs:", len(docs))

    for i, doc in enumerate(docs, 1):
        print(f"\n===== Chunk {i} =====")
        print(doc.page_content[:500])
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = template.invoke({
        'question':question,
        'context':context
    })
    
    response = llm_model.invoke(prompt)
    print("Bot : ", response.content)
    
    messages.append(("You :",question))
    messages.append(("Bot : ",response.content))
    
for role, message in messages:
    print(f"{role}:{message}")