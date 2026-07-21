from AI_Code_Assistant.config import SEARCH_TYPE, SEARCH_KWARGS
from langchain_core.vectorstores import VectorStoreRetriever

def get_retriever(vectordb) -> VectorStoreRetriever:
    
    return vectordb.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs=SEARCH_KWARGS
    )