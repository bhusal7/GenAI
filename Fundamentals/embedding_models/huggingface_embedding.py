from langchain_huggingface import HuggingFaceEmbeddings
# from dotenv import load_dotenv

# load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    'hello man',
    'hi women',
    'hahaha'
]

vector = embeddings.embed_documents(texts)

print(vector)
print("Dimension:", len(vector))