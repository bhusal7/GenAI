import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()


# Page setup

st.set_page_config(
    page_title="Legal Contract Risk Analyzer",
    page_icon="⚖️",
    layout="wide",
)


# Structured output schema (used only when a document is loaded)

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

DOC_SYSTEM_PROMPT = """
You are an expert Legal Contract Risk Analysis Assistant.

Your responsibility is to analyze only the provided contract context.

Identify potential legal, financial, compliance, or operational risks.

Focus on:
• Liability
• Indemnification
• Termination
• Confidentiality
• Intellectual Property
• Auto-renewal
• Non-compete
• Penalties
• Payment obligations
• Warranties
• Arbitration
• Governing law

Never invent information.

If the answer cannot be determined from the provided context, respond with:
"I cannot determine the answer from the provided contract."

Return the response strictly in the required JSON format.

{format_instructions}
"""

DOC_HUMAN_PROMPT = """
Contract Context:
{context}

User Question:
{question}

Analyze the contract carefully and answer using only the provided context.
"""

GENERAL_SYSTEM_PROMPT = """
You are a knowledgeable Legal & Contracts Assistant.

No contract document has been uploaded right now, so answer using your
general legal knowledge (contract law, common clauses, negotiation tips,
risk concepts such as liability, indemnification, termination,
confidentiality, IP, auto-renewal, non-compete, penalties, payment
obligations, warranties, arbitration, and governing law).

Be clear that this is general information, not a review of any specific
document, and remind the user (briefly, only if relevant) that this is not
a substitute for a licensed attorney's advice. Keep answers concise and
practical. If the user asks something totally unrelated to legal/contract
topics, you may still help, but gently note you're specialized for
contract & legal questions.
"""

doc_template = ChatPromptTemplate.from_messages(
    [("system", DOC_SYSTEM_PROMPT), ("human", DOC_HUMAN_PROMPT)]
)

general_template = ChatPromptTemplate.from_messages(
    [("system", GENERAL_SYSTEM_PROMPT), ("human", "{question}")]
)



# Cached resources

@st.cache_resource(show_spinner=False)
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatMistralAI(model="mistral-large-latest", temperature=0.2)



# Session state

if "messages" not in st.session_state:
    st.session_state.messages = []  # list[dict(role, content)]
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "source_label" not in st.session_state:
    st.session_state.source_label = None


def build_retriever_from_docs(docs, llm):
    splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_metadata={"hnsw:space": "cosine"},
    )

    base_retriever = vector_store.as_retriever()

    multi_query = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
    return multi_query


def format_risk_report(report: RiskReport) -> str:
    out = (
        f"**Contract Name:** {report.contract_name}\n\n"
        f"**Overall Risk Level:** {report.overall_risk_level}\n\n"
    )
    if report.risky_clauses:
        for i, clause in enumerate(report.risky_clauses, 1):
            out += (
                f"**Clause {i}**\n"
                f"- Text: {clause.clause_text}\n"
                f"- Risk Level: {clause.risk_level}\n"
                f"- Reason: {clause.reason}\n\n"
            )
    else:
        out += "_No specific risky clauses were flagged for this question._\n\n"
    out += f"**Recommendation:** {report.recommendation}"
    return out



# Sidebar - source selection

st.sidebar.title("⚖️ Document Source")
mode = st.sidebar.radio(
    "Choose how to chat:",
    ["Upload PDF", "Paste Web URL", "General Chat (no document)"],
    index=2,
)

llm = get_llm()

if mode == "Upload PDF":
    uploaded_file = st.sidebar.file_uploader("Upload a contract PDF", type=["pdf"])
    if uploaded_file and st.sidebar.button("Load PDF", use_container_width=True):
        with st.spinner("Reading and indexing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            st.session_state.retriever = build_retriever_from_docs(docs, llm)
            st.session_state.source_label = f"PDF: {uploaded_file.name}"
            st.session_state.messages = []
        st.sidebar.success("PDF loaded. Start chatting below!")

elif mode == "Paste Web URL":
    web_url = st.sidebar.text_input("Contract page URL", placeholder="https://example.com/contract")
    if web_url and st.sidebar.button("Load URL", use_container_width=True):
        with st.spinner("Fetching and indexing page..."):
            loader = WebBaseLoader(web_url)
            docs = loader.load()
            st.session_state.retriever = build_retriever_from_docs(docs, llm)
            st.session_state.source_label = f"URL: {web_url}"
            st.session_state.messages = []
        st.sidebar.success("Page loaded. Start chatting below!")

else:  # General Chat
    if st.session_state.retriever is not None:
        if st.sidebar.button("Clear loaded document & go General", use_container_width=True):
            st.session_state.retriever = None
            st.session_state.source_label = None
            st.session_state.messages = []
    st.sidebar.info(
        "No document needed here — ask general contract/legal questions "
        "and the bot will answer from its own knowledge."
    )

if st.session_state.source_label:
    st.sidebar.markdown(f"**Active source:** {st.session_state.source_label}")

if st.sidebar.button("🗑️ Reset chat history", use_container_width=True):
    st.session_state.messages = []

st.sidebar.caption(
    "Tip: Load a PDF or URL to get structured clause-by-clause risk analysis. "
    "Skip loading anything to just chat generally about contracts and legal topics."
)


# Main chat area

st.title("⚖️ Legal Contract Risk Analyzer")
st.caption(
    "Upload a PDF, paste a contract URL, or just chat directly — no document required."
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask about the contract, or ask a general legal question...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if st.session_state.retriever is not None:
                    # Document-grounded structured risk analysis
                    retrieved_docs = st.session_state.retriever.invoke(user_question)
                    context_str = "\n\n".join(d.page_content for d in retrieved_docs)

                    prompt = doc_template.invoke(
                        {
                            "context": context_str,
                            "question": user_question,
                            "format_instructions": format_instructions,
                        }
                    )
                    response = llm.invoke(prompt)
                    cleaned = response.content.replace("```json", "").replace("```", "").strip()

                    try:
                        report = parser.parse(cleaned)
                        answer = format_risk_report(report)
                    except Exception:
                        # Fall back to raw model output if it didn't match the schema
                        answer = response.content
                else:
                    # General conversational legal assistant, no document loaded
                    prompt = general_template.invoke({"question": user_question})
                    response = llm.invoke(prompt)
                    answer = response.content

            except Exception as e:
                answer = f"⚠️ Something went wrong: {e}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})