from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

load_dotenv()

# Load the PDF
loader = PyPDFLoader(
    "C:/Users/Acer/OneDrive/Desktop/GenAI/RAG/documents_loader/GRU.pdf"
)

docs = loader.load()

# Initialize Mistral Embeddings
embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

# Create Semantic Chunker
splitter = SemanticChunker(embeddings)

# Split the document semantically
chunks = splitter.split_documents(docs)

# Print the first chunk
print(chunks[0].page_content)

# Print total number of chunks
print("Total Chunks:", len(chunks))

