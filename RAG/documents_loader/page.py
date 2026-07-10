from langchain_community.document_loaders import WebBaseLoader

data = WebBaseLoader("https://www.apple.com/mac/")

docs = data.load()

print(docs[0].page_content)

print(len(docs))