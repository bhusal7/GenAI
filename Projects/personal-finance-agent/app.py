import os
import threading
import time

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

from tools.stock_tool import get_stock_price
from tools.news_tool import get_market_news

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🧠",
    layout="wide",
)

# ----------------------------------------------------------------------------
# Shared state object used to bridge the background agent thread and the
# Streamlit main thread. This replaces the original terminal `input()` call
# used for human-in-the-loop (HITL) tool approval, since a Streamlit app
# cannot block on `input()`. The approval logic/behavior itself (ask before
# every tool call, deny => "Tool call denied by user.") is unchanged.
# ----------------------------------------------------------------------------
class AgentBridge:
    def __init__(self):
        self.pending_tool = None      # dict: {"name": str, "args": dict, "id": str}
        self.decision_event = threading.Event()
        self.decision = None          # "yes" / "no"
        self.result = None
        self.error = None
        self.running = False
        self.log = []                 # list of dicts describing tool call events


if "bridge" not in st.session_state:
    st.session_state.bridge = AgentBridge()

if "messages" not in st.session_state:
    st.session_state.messages = []  # chat history: {"role": "user"/"assistant", "content": str}

if "auto_approve" not in st.session_state:
    st.session_state.auto_approve = False

bridge: AgentBridge = st.session_state.bridge


# ----------------------------------------------------------------------------
# 🧠 LLM Setup (unchanged)
# ----------------------------------------------------------------------------
@st.cache_resource
def get_llm():
    return ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.2,
    )


llm = get_llm()


# ----------------------------------------------------------------------------
# human-in-the-loop (HITL) middleware
# Same behavior as the original `human_approval`, but instead of blocking on
# `input()`, it publishes the pending tool call to the Streamlit UI and waits
# for the user to click Approve / Deny.
# ----------------------------------------------------------------------------
@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call."""
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call.get("args", {})

    if st.session_state.get("auto_approve"):
        bridge.log.append({"tool": tool_name, "args": tool_args, "decision": "auto-approved"})
        return handler(request)

    bridge.decision_event.clear()
    bridge.pending_tool = {"name": tool_name, "args": tool_args, "id": request.tool_call["id"]}

    # Block this background thread until the user approves/denies in the UI
    bridge.decision_event.wait()

    confirm = bridge.decision
    bridge.pending_tool = None
    bridge.log.append({"tool": tool_name, "args": tool_args, "decision": confirm})

    if confirm != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"],
        )

    return handler(request)


# ----------------------------------------------------------------------------
# creating agent (unchanged)
# ----------------------------------------------------------------------------
@st.cache_resource
def get_agent():
    return create_agent(
        llm,
        tools=[get_stock_price, get_market_news],
        system_prompt=(
            "You are a deep research assistant. When the user gives a topic, "
            "use the search_topic tool (call it 2-3 times with different angles "
            "of the topic if needed) to gather information, then write a clear "
            "summary with sources. If the user asks to save it, use save_report."
        ),
        middleware=[human_approval],
    )


agent = get_agent()


# ----------------------------------------------------------------------------
# Background worker that runs agent.invoke() so the Streamlit UI thread stays
# responsive and can show the HITL approval prompt while the agent is running.
# ----------------------------------------------------------------------------
def run_agent(query: str, bridge: AgentBridge):
    bridge.running = True
    bridge.error = None
    bridge.result = None
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        bridge.result = result["messages"][-1].content
    except Exception as e:
        bridge.error = str(e)
    finally:
        bridge.running = False
        bridge.pending_tool = None
        bridge.decision_event.set()  # release in case something is still waiting


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🧠 Deep Research Agent")
    st.caption("Type 'report: <topic>' to generate a full markdown research report")

    st.session_state.auto_approve = st.toggle(
        "Auto-approve tool calls",
        value=st.session_state.auto_approve,
        help="If off, you must approve every tool call the agent makes (human-in-the-loop), "
             "matching the original terminal app's behavior.",
    )

    st.divider()
    st.subheader("Environment")
    for var in ["ALPHAVANTAGE_API_KEY", "TAVILY_API_KEY", "MISTRAL_API_KEY"]:
        present = "✅" if os.getenv(var) else "❌"
        st.write(f"{present} `{var}`")

    st.divider()
    if bridge.log:
        st.subheader("Tool call log")
        for entry in bridge.log[-10:]:
            st.write(f"**{entry['tool']}**({entry['args']}) → `{entry['decision']}`")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.bridge = AgentBridge()
        st.rerun()


# ----------------------------------------------------------------------------
# Main chat area
# ----------------------------------------------------------------------------
st.title("Deep Research Agent")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("You: ", disabled=bridge.running)

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    thread = threading.Thread(target=run_agent, args=(query, bridge), daemon=True)
    thread.start()
    st.rerun()


# ----------------------------------------------------------------------------
# Fragment that polls the running agent thread for:
#  - a pending tool-call approval request -> show Approve / Deny buttons
#  - a finished result / error -> append to chat history
# This is what allows the blocking `human_approval` middleware (running on a
# background thread) to talk to the Streamlit UI.
# ----------------------------------------------------------------------------
@st.fragment(run_every=0.5)
def agent_status():
    bridge: AgentBridge = st.session_state.bridge

    if bridge.pending_tool is not None:
        pt = bridge.pending_tool
        with st.chat_message("assistant"):
            st.info(f"🔧 Agent wants to call **{pt['name']}** with args `{pt['args']}`. Approve?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"approve_{pt['id']}"):
                    bridge.decision = "yes"
                    bridge.decision_event.set()
                    st.rerun()
            with col2:
                if st.button("❌ Deny", key=f"deny_{pt['id']}"):
                    bridge.decision = "no"
                    bridge.decision_event.set()
                    st.rerun()
        return

    if bridge.running:
        with st.chat_message("assistant"):
            st.spinner("Agent is thinking...")
        return

    if bridge.result is not None:
        st.session_state.messages.append({"role": "assistant", "content": bridge.result})
        bridge.result = None
        st.rerun()

    if bridge.error is not None:
        st.session_state.messages.append(
            {"role": "assistant", "content": f"⚠️ Error: {bridge.error}"}
        )
        bridge.error = None
        st.rerun()


agent_status()