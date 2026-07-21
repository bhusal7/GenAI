from langchain_community.document_loaders import PyPDFLoader

# using Token_Text_Splitter
from langchain_text_splitters import TokenTextSplitter

# using Recursive_Text_Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter # - it focus on meaning more than chunks so it is far more better

data = PyPDFLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/RAG/documents_loader/GRU.pdf")
docs = data.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 10
)

chunks = splitter.split_documents(docs)

print(chunks[0].page_content)
print(len(chunks))


print('Docs: ',docs)
print("Docs Len:",len(docs))
print('Docs: ',docs[14])


