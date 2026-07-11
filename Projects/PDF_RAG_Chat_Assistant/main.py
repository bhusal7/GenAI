from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv() 

embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    persist_directory = "chroma_db",
    embedding_function = embedding_model
)


retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5  # it has value 0 & 1 : 0 -> more diverse result and 1 -> 0 -> less diverse result 
    }
)

llm = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.9
)


# prompt templete
prompt = ChatPromptTemplate.from_messages([
    ('system',"""
     Yor're a helpful AI Assistant.
     
Use only the provided context to answer the questions.

If the answer isn't present in the context,
say: "I can't find the answer in the document."
     """
     ),
    ('human',"""
     Context:{context}
     Question:{question}
     """
     )
])

print("======== -------- RAG System Created ---------- =========")
print("<<<<<<<<<<<<<<<<< Print 'O' to exit >>>>>>>>>>>>>>>>>>>")

while True:
    query = input("You : ")
    if query == '0':
        break
    
    docs = retriever.invoke(query)
    
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    
    final_prompt = prompt.invoke({
        'context' : context,
        "question" : query
    })
    
    response = llm.invoke(final_prompt)
    
    print(f"\n AI : {response.content}") 