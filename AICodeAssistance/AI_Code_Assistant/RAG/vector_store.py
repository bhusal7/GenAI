from langchain_chroma import Chroma
from config import PERSIST_DIRECTORY,embeddings
from RAG.embeddings import get_embeddings

def create_chroma_db(chunks):
        
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,  # <-- Added () here
        persist_directory=PERSIST_DIRECTORY,
        collection_name="ai_code_assistant"
)
    
    return vectordb