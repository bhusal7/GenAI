from dotenv import load_dotenv
load_dotenv() 

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

model = ChatMistralAI(
    model = "mistral-large-latest",
    temperature=0.9
)


# save the response inside list bcz model must known abt the chat history so :- 

print("Choose your AI mode : ")
print("Press 1 for angry mode.")
print("Press 2 for Funny mode.")
print("Press 3 for Sad mode.")

choice = int(input("Tell your response :- "))

if choice == 1:
    mode = "Yor're an angry AI Agent. You respond aggressively & impatiently"
elif choice == 2:
    mode = "Yor're an funny AI Agent. You respond humor & jokes"
elif choice == 3:
    mode = "Yor're an sad AI Agent. You respond sadly & emotionly"

messages = [
    SystemMessage(content=mode)  # yo line le aba hamro AI lai jaile funny/sad/angry way ma text garna train/assist garcha
    
]

print("------------------- Welcome type 0 to exit the application-----------------------------")
while True:
    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))    # for msg history
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))   # for msg history
    print("Bot : ", response.content)
    
print("Messages History : ", messages)