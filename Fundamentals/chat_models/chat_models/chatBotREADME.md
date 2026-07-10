# 🤖 Mood-Based AI Chatbot (CLI Version)

A command-line chatbot built using LangChain and Mistral AI that allows users to interact with an AI assistant in different moods.

The chatbot maintains conversation history and responds according to the selected personality throughout the session.

## Features

* Three AI personalities

  * 🔥 Angry
  * 🤡 Funny
  * 🌧️ Sad
* Maintains chat history
* Uses LangChain message objects
* Simple terminal-based interface
* Powered by Mistral AI

## Technologies Used

* Python
* LangChain
* Mistral AI
* python-dotenv

## Project Structure

```text
chatbot.py
requirements.txt
.env
README.md
```

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key_here
```

## Run the Application

```bash
python chatbot.py
```

## How It Works

1. Select a mood for the AI.
2. A System Message is created based on the selected mood.
3. User messages are stored as Human Messages.
4. AI responses are stored as AI Messages.
5. The entire message history is sent to the model for context-aware conversations.

## Available Modes

| Option | Mood     |
| ------ | -------- |
| 1      | Angry 🔥 |
| 2      | Funny 🤡 |
| 3      | Sad 🌧️  |

## Learning Concepts

* Chat Models
* SystemMessage
* HumanMessage
* AIMessage
* Message History
* Stateful Conversations

## License

This project is created for learning and educational purposes.
