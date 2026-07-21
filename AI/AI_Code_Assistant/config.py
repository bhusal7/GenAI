from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

mistral_llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0
)

groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=20
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

PERSIST_DIRECTORY = "chroma_db"

SEARCH_TYPE = "mmr"

SEARCH_KWARGS = {
    'k':5,
    'fetch_k':20
}

TEMPERATURE = 0