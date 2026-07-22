import langchain
print(langchain.__version__)

# Update these two lines to import from langchain_classic
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from config import mistral_llm

def get_multi_query_retriever(retriever):
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=retriever,
        llm=mistral_llm
    )
    return multi_query_retriever