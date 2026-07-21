from RAG.indexing import build_rag
from Tools import set_retriever

retriever = build_rag("data")
set_retriever(retriever)