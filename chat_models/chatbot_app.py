import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Moodcast AI", page_icon="🎭", layout="centered")

# ----------------------------------------------------------------------------
# Mode definitions — same prompts/roles as the original script
# ----------------------------------------------------------------------------
MODES = {
    "angry": {
        "label": "Angry",
        "emoji": "🔥",
        "tagline": "Short fuse. Zero patience.",
        "system": "Yor're an angry AI Agent. You respond aggressively & impatiently",
        "accent": "#FF3B30",
        "accent_soft": "#3a1210",
        "bg": "#160707",
        "panel": "#1f0b0b",
        "text": "#FCEAE7",
        "font": "'Oswald', sans-serif",
    },
    "funny": {
        "label": "Funny",
        "emoji": "🤡",
        "tagline": "Jokes first, sense later.",
        "system": "Yor're an funny AI Agent. You respond humor & jokes",
        "accent": "#FFB703",
        "accent_soft": "#3a2c05",
        "bg": "#151006",
        "panel": "#211808",
        "text": "#FFF3D6",
        "font": "'Fredoka', sans-serif",
    },
    "sad": {
        "label": "Sad",
        "emoji": "🌧️",
        "tagline": "Everything, but heavier.",
        "system": "Yor're an sad AI Agent. You respond sadly & emotionly",
        "accent": "#6C8EF5",
        "accent_soft": "#141c33",
        "bg": "#0a0d16",
        "panel": "#101526",
        "text": "#E3E7F5",
        "font": "'Source Serif 4', serif",
    },
}

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "mode_key" not in st.session_state:
    st.session_state.mode_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []

model = ChatMistralAI(model="mistral-large-latest", temperature=0.9)

# ----------------------------------------------------------------------------
# Global styles
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Oswald:wght@500;700&family=Fredoka:wght@400;600&family=Source+Serif+4:ital,wght@0,400;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2.5rem; max-width: 760px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SCREEN 1 — Mode selection
# ----------------------------------------------------------------------------
if st.session_state.mode_key is None:
    st.markdown(
        """
        <style>
        .stApp { background: #0b0b0f; }
        .hero-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.35em;
            font-size: 0.72rem;
            color: #8b8b95;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            color: #f5f5f7;
            line-height: 1.05;
            margin-bottom: 0.4rem;
        }
        .hero-sub {
            color: #9a9aa5;
            font-size: 1.02rem;
            margin-bottom: 2.4rem;
        }
        div[data-testid="column"] {
            background: #131318;
            border: 1px solid #23232b;
            border-radius: 14px;
            padding: 1.6rem 1.3rem 1.3rem 1.3rem;
            transition: border-color 0.15s ease;
        }
        div[data-testid="column"]:hover { border-color: #3a3a45; }
        .mode-emoji { font-size: 2.1rem; margin-bottom: 0.5rem; }
        .mode-name {
            font-size: 1.25rem;
            font-weight: 700;
            color: #f5f5f7;
            margin-bottom: 0.15rem;
        }
        .mode-tag {
            color: #8b8b95;
            font-size: 0.88rem;
            margin-bottom: 1.1rem;
            min-height: 2.2em;
        }
        div[data-testid="stButton"] > button {
            width: 100%;
            border-radius: 8px;
            border: 1px solid #33333d;
            background: #1a1a20;
            color: #f0f0f2;
            font-weight: 500;
            padding: 0.5rem 0;
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #55555f;
            background: #202027;
            color: #fff;
        }
        </style>

        <div class="hero-eyebrow">MOODCAST · 01 / 03 MOODS AVAILABLE</div>
        <div class="hero-title">Pick the AI's mood.</div>
        <div class="hero-sub">One model, three temperaments. The mood you choose becomes the personality for the whole conversation.</div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, key in zip(cols, MODES.keys()):
        m = MODES[key]
        with col:
            st.markdown(f'<div class="mode-emoji">{m["emoji"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mode-name">{m["label"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mode-tag">{m["tagline"]}</div>', unsafe_allow_html=True)
            if st.button("Enter", key=f"pick_{key}"):
                st.session_state.mode_key = key
                st.session_state.messages = [SystemMessage(content=m["system"])]
                st.rerun()

# ----------------------------------------------------------------------------
# SCREEN 2 — Chat
# ----------------------------------------------------------------------------
else:
    m = MODES[st.session_state.mode_key]

    st.markdown(
        f"""
        <style>
        .stApp {{ background: {m['bg']}; }}
        .block-container {{ padding-top: 1.6rem; }}

        .mood-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid {m['accent_soft']};
            padding-bottom: 1rem;
            margin-bottom: 1.4rem;
        }}
        .mood-header-left {{ display: flex; align-items: center; gap: 0.7rem; }}
        .mood-badge {{
            font-size: 1.6rem;
            background: {m['accent_soft']};
            border-radius: 10px;
            padding: 0.4rem 0.6rem;
        }}
        .mood-title {{
            font-family: {m['font']};
            font-weight: 700;
            font-size: 1.4rem;
            color: {m['text']};
            margin: 0;
        }}
        .mood-caption {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {m['accent']};
            margin: 0;
        }}

        div[data-testid="stChatMessage"] {{
            background: {m['panel']};
            border: 1px solid {m['accent_soft']};
            border-radius: 12px;
            padding: 0.3rem 0.4rem;
        }}
        div[data-testid="stChatMessage"] p {{
            color: {m['text']};
            font-family: {m['font']};
        }}

        div[data-testid="stChatInput"] textarea {{
            background: {m['panel']} !important;
            color: {m['text']} !important;
            border: 1px solid {m['accent_soft']} !important;
        }}

        div[data-testid="stButton"] > button {{
            border-radius: 8px;
            border: 1px solid {m['accent_soft']};
            background: transparent;
            color: {m['accent']};
            font-size: 0.82rem;
            padding: 0.3rem 0.8rem;
        }}
        div[data-testid="stButton"] > button:hover {{
            border-color: {m['accent']};
            color: {m['text']};
        }}
        </style>

        <div class="mood-header">
            <div class="mood-header-left">
                <div class="mood-badge">{m['emoji']}</div>
                <div>
                    <p class="mood-title">{m['label']} mode</p>
                    <p class="mood-caption">moodcast · live session</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([5, 1])
    with right:
        if st.button("Switch mood"):
            st.session_state.mode_key = None
            st.session_state.messages = []
            st.rerun()

    # render chat history (SystemMessage is never shown)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar=m["emoji"]):
                st.write(msg.content)

    prompt = st.chat_input(f"Say something to the {m['label'].lower()} agent...")

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))  # for msg history
        with st.chat_message("user"):
            st.write(prompt)

        response = model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))  # for msg history

        with st.chat_message("assistant", avatar=m["emoji"]):
            st.write(response.content)

    with st.expander("Messages history"):
        st.write(st.session_state.messages)