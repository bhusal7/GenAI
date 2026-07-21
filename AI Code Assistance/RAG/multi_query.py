from multi_query import MultiQueryRetriever
from AI_Code_Assistant.config import mistral_llm

def get_multi_query_retriever(retriever):
    
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=retriever,
        llm=mistral_llm
    )
    
    return multi_query_retriever