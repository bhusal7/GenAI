# 🎭 Moodcast AI (Streamlit Version)

Moodcast AI is a Streamlit-based chatbot that allows users to chat with an AI assistant in different personalities.

Users can choose between Angry, Funny, and Sad modes, and the AI maintains the selected personality throughout the conversation.

## Features

* Modern Streamlit UI
* Three unique AI personalities
* Real-time chat interface
* Chat history support
* Mood switching
* Custom styling for each personality
* Powered by LangChain and Mistral AI

## Technologies Used

* Python
* Streamlit
* LangChain
* Mistral AI
* python-dotenv

## Project Structure

```text
app.py
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
streamlit run app.py
```

## Available Modes

### 🔥 Angry Mode

* Aggressive responses
* Impatient personality
* Red-themed interface

### 🤡 Funny Mode

* Humorous replies
* Joke-oriented personality
* Yellow-themed interface

### 🌧️ Sad Mode

* Emotional responses
* Melancholic personality
* Blue-themed interface

## How It Works

1. Select an AI personality.
2. The selected mood is stored as a System Message.
3. Messages are stored in Streamlit Session State.
4. Conversation history is passed to the model on every interaction.
5. The AI responds according to the chosen personality.

## Learning Concepts

* Streamlit Chat UI
* Session State
* Chat Models
* System Messages
* Human Messages
* AI Messages
* Context-Aware Conversations
* Custom Streamlit Styling

## License

This project is created for learning and educational purposes.
