from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=64
)

texts = [
    'hello man',
    'hi women',
    'hahaha'
]

vector = embeddings.embed_query(texts)

print(vector)
print("Dimension:", len(vector))