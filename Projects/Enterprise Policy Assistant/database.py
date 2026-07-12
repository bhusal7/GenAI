from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

data = PyPDFLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/Projects/Company/Company_Policy_Assistant_about_AIML.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1400,
    chunk_overlap = 140
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory = "chroma_db"
)

print("Pages loaded:", len(docs))
print("Chunks created:", len(chunks))
print("Documents in DB:", vector_store._collection.count())
