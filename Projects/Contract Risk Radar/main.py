from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

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

pdf_path = "C:/Users/Acer/OneDrive/Desktop/GenAI/Projects/NewProject/Rag_Project.pdf"
web_url = "https://legaltemplates.net/form/business-contract/"

src_type = "pdf"

if src_type == "pdf":
    data = PyPDFLoader(pdf_path)
    docs = data.load()
else:
    data = WebBaseLoader(web_url)
    docs = data.load()


splitter = TokenTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db",
    collection_metadata={"hnsw:space": "cosine"}
)

retriever = vector_store.as_retriever()

llm_model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.2
)

multi_query = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm_model
)

template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
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
    ),

    (
        "human",
        """
Contract Context:
{context}

User Question:
{question}

Analyze the contract carefully and answer using only the provided context.
"""
    )
])

chain = template | llm_model

messages = []

print("============== LEGAL CONTRACT RISK ANALYZER (RAG)=================")

print("------------ Ask any question about the loaded contract-----------------")

print('************ Type "exit" to close the application ******************')
while True:
    question = input("You : ")

    if question.lower() == "exit":
        break

    messages.append(HumanMessage(content=question))

    retrieved_docs = multi_query.invoke(question)
    context_str = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = template.invoke({
        "context": context_str,
        "question": question,
        "format_instructions": format_instructions
    })

    response = llm_model.invoke(prompt)

    parse_respond = parser.parse(
        response.content.replace("```json", "").replace("```", "").strip()
    )

    formatted_response = (
        f"Contract Name: {parse_respond.contract_name}\n"
        f"Overall Risk Level: {parse_respond.overall_risk_level}\n\n"
    )

    for i, clause in enumerate(parse_respond.risky_clauses, 1):
        formatted_response += (
            f"Clause {i}\n"
            f"Clause Text: {clause.clause_text}\n"
            f"Risk Level: {clause.risk_level}\n"
            f"Reason: {clause.reason}\n\n"
        )

    formatted_response += f"Recommendation: {parse_respond.recommendation}"

    print("Bot:")
    print(formatted_response)

    messages.append(AIMessage(content=formatted_response))
    
print("\n=================== CHAT HISTORY LOG ===================")
for msg in messages:
    role = "You" if isinstance(msg, HumanMessage) else "Bot"
    print(f"{role}: {msg.content}")
