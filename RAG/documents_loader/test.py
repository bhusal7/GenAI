from langchain_community.document_loaders import TextLoader

# using Character_Text_Splitter
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="",
    chunk_size = 10,
    chunk_overlap = 1,
)

data = TextLoader("C:/Users/Acer/OneDrive/Desktop/GenAI/RAG/documents_loader/notes.txt") 

docs = data.load()

chunks = splitter.split_documents(docs)
print(chunks)
print(len(chunks))

print("======== Printing !0,10 chunks like : 'hello how ': is has 10 chunks means it index=10 ===============")
for i in chunks:
    print(i.page_content)
    print()
    print()
    print()

print("It only print Page_content:",docs[0].page_content)
print("\nIt only print Meta_Data:",docs[0].metadata)
print("\nLength od Docs : ",len(docs))

