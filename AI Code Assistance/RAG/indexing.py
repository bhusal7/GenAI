from .loader import load_code_directory,load_single_file
from .multi_query import get_multi_query_retriever
from .retriever import get_retriever
from .splitter import split_documents
from .vector_store import create_chroma_db

def build_rag(directory_path : str):
    
    documents = load_code_directory(directory_path)
    
    chunks = split_documents(documents)
    
    vectordb = create_chroma_db(chunks)
    
    retriever = get_retriever(vectordb)
    
    multi_query_retriever = get_multi_query_retriever(retriever)
    
    return multi_query_retriever