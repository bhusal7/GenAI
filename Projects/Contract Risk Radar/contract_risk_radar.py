"""
Contract Risk Radar
=====================
Reads a legal contract (from a local PDF OR a web page URL), scans it for
risky clauses, and outputs a structured, validated risk report.

This script is written in PLAIN SEQUENTIAL STYLE (no functions) so that
reading it top-to-bottom IS the pipeline:

    PyPDFLoader / WebBaseLoader  ->  TokenTextSplitter  ->  HuggingFace Embeddings
    ->  Chroma VectorStore  ->  MultiQueryRetriever
    ->  SystemMessage/HumanMessage  ->  ChatModel
    ->  PydanticOutputParser  ->  Structured RiskReport

Install:
  pip install langchain langchain-community langchain-openai langchain-chroma
  pip install sentence-transformers chromadb pypdf tiktoken pydantic bs4
"""

import os
from typing import List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser


# ---------------------------------------------------------------------------
# STEP 0 — Define the structured output schema (Pydantic BaseModel)
# ---------------------------------------------------------------------------
class RiskClause(BaseModel):
    clause_text: str = Field(description="The exact clause text found risky")
    risk_level: str = Field(description="One of: LOW, MEDIUM, HIGH, CRITICAL")
    reason: str = Field(description="Why this clause is risky")


class RiskReport(BaseModel):
    contract_name: str = Field(description="Name/title of the contract")
    overall_risk_level: str = Field(description="Overall risk: LOW, MEDIUM, HIGH, CRITICAL")
    risky_clauses: List[RiskClause] = Field(description="List of flagged risky clauses")
    recommendation: str = Field(description="Overall recommendation for the reviewer")


parser = PydanticOutputParser(pydantic_object=RiskReport)
format_instructions = parser.get_format_instructions()


# ---------------------------------------------------------------------------
# STEP 1 — Choose contract SOURCE: "pdf" (local file) or "web" (URL)
# ---------------------------------------------------------------------------
source_type = "pdf"   # <-- change to "web" to load a contract from a URL instead

pdf_path = "sample_contract.pdf"                       # used when source_type = "pdf"
web_url = "https://example.com/sample-contract-page"   # used when source_type = "web"


# ---------------------------------------------------------------------------
# STEP 2 — DocumentLoader: PyPDFLoader OR WebBaseLoader
# ---------------------------------------------------------------------------
if source_type == "pdf":
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    contract_name = pdf_path
    print(f"[Step 2 - Loader] Loaded {len(documents)} pages from PDF '{pdf_path}'")
else:
    loader = WebBaseLoader(web_paths=[web_url])
    documents = loader.load()
    contract_name = web_url
    print(f"[Step 2 - Loader] Loaded {len(documents)} page(s) from URL '{web_url}'")


# ---------------------------------------------------------------------------
# STEP 3 — TextSplitter: TokenTextSplitter breaks content into token-based chunks
# ---------------------------------------------------------------------------
splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)

print(f"[Step 3 - Splitter] Created {len(chunks)} token-based chunks")


# ---------------------------------------------------------------------------
# STEP 4 — Embeddings: HuggingFace embedding model
# ---------------------------------------------------------------------------
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("[Step 4 - Embeddings] HuggingFace embedding model loaded")


# ---------------------------------------------------------------------------
# STEP 5 — VectorStore: Chroma stores the embedded chunks (HNSW indexing)
# ---------------------------------------------------------------------------
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_contract_risk_db",
    collection_metadata={"hnsw:space": "cosine"},
)

print("[Step 5 - VectorStore] Chroma index built with HNSW cosine space")


# ---------------------------------------------------------------------------
# STEP 6 — Chat model to power query rewriting + final analysis
# ---------------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print("[Step 6 - ChatModel] LLM initialized")


# ---------------------------------------------------------------------------
# STEP 7 — Retriever: MultiQueryRetriever wraps the base Chroma retriever
# ---------------------------------------------------------------------------
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm,
)

print("[Step 7 - Retriever] MultiQueryRetriever ready")


# ---------------------------------------------------------------------------
# STEP 8 — Retrieve relevant clauses for risk analysis
# ---------------------------------------------------------------------------
question = "Find clauses related to liability, termination, penalties, indemnity, and auto-renewal risks."

retrieved_docs = retriever.invoke(question)
context = "\n\n".join(doc.page_content for doc in retrieved_docs)

print(f"[Step 8 - Retrieval] Retrieved {len(retrieved_docs)} relevant chunks")


# ---------------------------------------------------------------------------
# STEP 9 — Build messages: SystemMessage + HumanMessage
# ---------------------------------------------------------------------------
system_message = SystemMessage(
    content=(
        "You are a legal risk analyst AI. Analyze the given contract excerpts "
        "and identify risky clauses (liability, termination, penalty, indemnity, "
        "auto-renewal, non-compete, etc.). Be precise and evidence-based. "
        f"Respond strictly in this JSON format:\n{format_instructions}"
    )
)

human_message = HumanMessage(
    content=(
        f"Contract name: {contract_name}\n\n"
        f"Relevant contract excerpts:\n{context}\n\n"
        f"Task: {question}"
    )
)

print("[Step 9 - Messages] System and Human messages constructed")


# ---------------------------------------------------------------------------
# STEP 10 — Call the chat model
# ---------------------------------------------------------------------------
response = llm.invoke([system_message, human_message])

print("[Step 10 - LLM Call] Response received from chat model")


# ---------------------------------------------------------------------------
# STEP 11 — Parse the raw LLM output into a validated Pydantic object
# ---------------------------------------------------------------------------
risk_report = parser.parse(response.content)

print("[Step 11 - Parser] LLM output validated into RiskReport object")


# ---------------------------------------------------------------------------
# STEP 12 — Final structured output
# ---------------------------------------------------------------------------
print("\n===== CONTRACT RISK REPORT =====")
print(risk_report.model_dump_json(indent=2))
