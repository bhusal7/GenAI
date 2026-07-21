from langchain_chroma import Chroma
from AI_Code_Assistant.config import PERSIST_DIRECTORY
from RAG.embeddings import get_embeddings

def create_chroma_db(chunks):
    embedding_model = get_embeddings()
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    return vectordb