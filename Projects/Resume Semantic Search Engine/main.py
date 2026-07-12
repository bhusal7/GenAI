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

templete = ChatPromptTemplate([
    (
        "system",
        """
You are an intelligent AI assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use outside knowledge.
- If the answer is not present in the context, respond:
  "I couldn't find that information in the provided document."
- Be accurate, concise, and professional.
"""
    ),
    (
        "human",
        """
Context:
{context}

Question:
{question}

Answer:
"""
    )
])

messages = []

print("------------ Research Paper ChatBox---------------\n")
print("********* Print 'exit' to Quit the App ******************\n")

while True:
    question = input("You : ")
    if question.lower() == "exit":
        break
    
    docs = retriever.invoke(question)
    print("\n===== Retrieved Chunks =====")
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}:")
        print(doc.page_content[:500])

    print("============================\n")
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = templete.invoke({
        "question":question,
        "context":context
    })
    
    response = llm_model.invoke(prompt)
    print("Bot : ",response.content)
    
    messages.append(("You : ",question))
    messages.append(("Bot : ", response.content))
    
for role,message in messages:
    print(f"{role}:{message}")
    