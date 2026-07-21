"""
=====================================================================
 CITY INTELLIGENCE AGENT — STREAMLIT UI
=====================================================================
Run with:
    streamlit run app.py

Talks to city_intelligence_create_agent.chain (a LangGraph agent with
interrupt-based human approval). No agent/tool features were changed —
only the human-approval pause was made web-safe (see comments in that
file) and the input format was fixed to match what create_agent expects.
=====================================================================
"""

import os
import uuid

import streamlit as st
from langgraph.types import Command

from city_intelligence_create_agent import chain

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CITY-INTEL // AGENT",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# "HACKER TERMINAL" THEME
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #0f1b12 0%, #05070a 55%, #030405 100%);
        color: #c9f7d6;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg, rgba(0,255,140,0.02) 0px, rgba(0,255,140,0.02) 1px,
            transparent 1px, transparent 3px
        );
        pointer-events: none;
        z-index: 0;
    }

    h1, h2, h3 { color: #39ff88 !important; letter-spacing: 1px; }

    .title-block {
        border: 1px solid #1f3d2a;
        border-radius: 6px;
        padding: 18px 22px;
        background: linear-gradient(180deg, rgba(20,40,25,0.55), rgba(5,10,7,0.6));
        box-shadow: 0 0 24px rgba(57,255,136,0.08), inset 0 0 40px rgba(57,255,136,0.03);
        margin-bottom: 14px;
    }
    .title-block h1 {
        margin: 0;
        font-size: 1.7rem;
        text-shadow: 0 0 12px rgba(57,255,136,0.55);
    }
    .title-block p {
        margin: 4px 0 0 0;
        color: #6fae87;
        font-size: 0.85rem;
    }

    section[data-testid="stSidebar"] {
        background: #04070a;
        border-right: 1px solid #163b24;
    }
    section[data-testid="stSidebar"] * { color: #9fe8bb !important; }
    section[data-testid="stSidebar"] hr { border-color: #163b24; }

    .status-ok   { color: #39ff88 !important; font-weight: 700; }
    .status-fail { color: #ff4d5e !important; font-weight: 700; }

    [data-testid="stChatMessage"] {
        border: 1px solid #1f3d2a;
        border-radius: 8px;
        background: rgba(10, 22, 14, 0.65);
        box-shadow: 0 0 14px rgba(57,255,136,0.05);
    }

    [data-testid="stChatInput"] textarea {
        background: #050a06 !important;
        color: #c9f7d6 !important;
        border: 1px solid #2a5c3a !important;
    }

    .alert-box {
        border: 1px solid #ff9d3d;
        border-radius: 8px;
        padding: 14px 18px;
        background: rgba(60, 35, 5, 0.35);
        color: #ffcf8f;
        box-shadow: 0 0 18px rgba(255,157,61,0.15);
        margin-bottom: 10px;
        line-height: 1.6;
    }
    .alert-box b { color: #ffb35c; }

    .stButton > button {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        border-radius: 6px;
        border: 1px solid #2a5c3a;
        background: #0b1a10;
        color: #39ff88;
        transition: all 0.15s ease-in-out;
    }
    .stButton > button:hover {
        background: #123321;
        border-color: #39ff88;
        box-shadow: 0 0 10px rgba(57,255,136,0.35);
        color: #baffd6;
    }

    .tool-pill {
        display: inline-block;
        border: 1px solid #2a5c3a;
        border-radius: 20px;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        font-size: 0.75rem;
        color: #9fe8bb;
        background: rgba(57,255,136,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None

config = {"configurable": {"thread_id": st.session_state.thread_id}}


def resolve(result):
    """Inspect the chain's output: either stash a pending approval
    request, or append the final assistant reply to chat history."""
    if isinstance(result, dict) and "__interrupt__" in result:
        st.session_state.pending = result
    else:
        answer = result["messages"][-1].content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.pending = None


# ---------------------------------------------------------------------------
# SIDEBAR — SYSTEM STATUS PANEL
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛰️ SYSTEM STATUS")

    def status_line(label, ok):
        css = "status-ok" if ok else "status-fail"
        badge = "ONLINE" if ok else "MISSING"
        st.markdown(f"`{label:<10}` <span class='{css}'>● {badge}</span>", unsafe_allow_html=True)

    status_line("MISTRAL", bool(os.getenv("MISTRAL_API_KEY")))
    status_line("WEATHER", bool(os.getenv("OPENWEATHER_API_KEY")))
    status_line("TAVILY", bool(os.getenv("TAVILY_API_KEY")))

    st.markdown("---")
    st.markdown("### 🧰 ACTIVE TOOLS")
    st.markdown(
        "<span class='tool-pill'>get_weather()</span>"
        "<span class='tool-pill'>get_news()</span>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🔐 HUMAN-IN-THE-LOOP")
    st.caption("Every tool call requires manual approval before execution.")

    st.markdown("---")
    st.markdown("### 🧵 SESSION")
    st.code(st.session_state.thread_id[:13], language="text")

    st.markdown("---")
    if st.button("🗑️  RESET SESSION", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="title-block">
        <h1>🛰️ CITY INTELLIGENCE AGENT</h1>
        <p>LangChain × LangGraph × Mistral — human-approved tool execution</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# PENDING APPROVAL  vs  CHAT INPUT
# ---------------------------------------------------------------------------
if st.session_state.pending:
    payload = st.session_state.pending["__interrupt__"][0].value

    st.markdown(
        f"""
        <div class="alert-box">
        ⚠️ <b>APPROVAL REQUIRED</b><br>
        TOOL &nbsp;: <b>{payload['tool']}</b><br>
        ARGS &nbsp;: <code>{payload['args']}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅  APPROVE", use_container_width=True):
            with st.spinner("⚙️ executing tool..."):
                result = chain.invoke(Command(resume="yes"), config=config)
            resolve(result)
            st.rerun()
    with col2:
        if st.button("⛔  DENY", use_container_width=True):
            with st.spinner("↩️ skipping tool call..."):
                result = chain.invoke(Command(resume="no"), config=config)
            resolve(result)
            st.rerun()
else:
    user_input = st.chat_input("Ask about a city's weather or news...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        with st.spinner("🔎 agent thinking..."):
            # create_agent expects {"messages": [...]}, not a raw string.
            result = chain.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config,
            )

        resolve(result)
        st.rerun()