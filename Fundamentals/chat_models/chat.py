
from dotenv import load_dotenv

# Universal Model Initialization
from langchain.chat_models import init_chat_model

# Provider-specific Model Classes
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ==========================================================
# 1(a). OpenAI - init_chat_model()
# ==========================================================

model = init_chat_model(
    model="gpt-5.5",
    model_provider="openai"
)

response = model.invoke("What is your name?")
print(response.content)


# ==========================================================
# 1(b). OpenAI - ChatOpenAI
# ==========================================================

model = ChatOpenAI(
    model="gpt-5.5"
)

response = model.invoke("From which country does Ronaldo belong?")
print(response.content)


# ==========================================================
# 2(a). Groq - init_chat_model()
# ==========================================================

model = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq"
)

response = model.invoke("What is cricket?")
print(response.content)


# ==========================================================
# 2(b). Groq - ChatGroq
# ==========================================================

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=20
)

response = model.invoke("What is cricket?")
print(response.content)


# ==========================================================
# 3(a). Google Gemini - init_chat_model()
# ==========================================================

model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai"
)

response = model.invoke(
    "Who is Ronaldo R9 of Brazil? Describe him in 9 points."
)

print(response.content)


# ==========================================================
# 3(b). Google Gemini - ChatGoogleGenerativeAI
# ==========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

response = model.invoke(
    "Who is Ronaldo R9 of Brazil? Describe him in 9 points."
)

print(response.content)


# ==========================================================
# 4(a). Mistral - init_chat_model()
# ==========================================================

model = init_chat_model(
    model="mistral-large-latest",
    model_provider="mistralai"
)

response = model.invoke(
    "Who is the Prime Minister of Nepal?"
)

print(response.content)


# ==========================================================
# 4(b). Mistral - ChatMistralAI
# ==========================================================

model = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0
)

response = model.invoke("Write a Poem on GenAI?")
print(response.content)
