from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

data = PyPDFLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/Projects/Multiple Resume PDFs/GenAI_Engineer.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1200,
    chunk_overlap = 120
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=r"chroma_db"
)

print("Pages:", len(docs))
print("Chunks:", len(chunks))
print("Stored:", vector_store._collection.count())