from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

docs = [
    Document(
        page_content="Artificial Intelligence (AI) enables machines to perform tasks that normally require human intelligence.",
        metadata={"topic": "AI"}
    ),
    Document(
        page_content="Machine Learning (ML) is a subset of AI that learns patterns from data to make predictions and decisions.",
        metadata={"topic": "ML"}
    ),
    Document(
        page_content="Deep Learning (DL) is a subset of ML that uses multi-layer neural networks to solve complex problems.",
        metadata={"topic": "DL"}
    )
]

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    
    # creating directory to Save
    persist_directory = "chroma_db"
)

# after learning ChromaDB we have to retrieve some Info....
    # kei Info Nikalna parcha
# so use 'Retrivers'

# ............... vector_store is responsible for Retrieving Info but LLM is responsible for answering our Questions...............
result = vector_store.similarity_search("what's Data Engineer?",k = 2)  # k = 2 means , how much result we want

for r in result:
    print(r.page_content)
    print(r.metadata)
    
retriver = vector_store.as_retriever()
# yaha as_retriever() vitra kai use vako chaina so yo "Similarity Search" strategy ko Algo. ho

docs = retriver.invoke("Explain AI Agents.")

for d in docs:
    print(d.page_content)


