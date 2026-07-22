import streamlit as st
from pipeline import run_code_assistant_pipeline

st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ---------------- #

st.sidebar.title("🤖 AI Code Assistant")
st.sidebar.markdown("---")

st.sidebar.info(
"""
### Features

✅ RAG Search

✅ Multi-Agent AI

✅ Bug Detection

✅ Optimization Suggestions

✅ Documentation Generator

✅ Explainable AI

✅ Critic Agent

✅ Automatic Report Saving
"""
)

st.sidebar.markdown("---")
st.sidebar.success("Built using LangChain + Mistral + Streamlit")

# ---------------- Main Header ---------------- #

st.title("🤖 AI Code Assistant Pro")

st.markdown(
"""
Ask anything about your codebase.

Examples:

- Explain authentication.py
- Find bugs in app.py
- Optimize my API
- Generate documentation
- Explain project architecture
"""
)

query = st.text_area(
    "Enter your Question",
    height=150,
    placeholder="Example: Explain login.py and suggest improvements..."
)

run = st.button("🚀 Analyze Code", use_container_width=True)

# ---------------- Run Pipeline ---------------- #

if run:

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    progress = st.progress(0)

    status = st.empty()

    with st.spinner("Running AI Agents..."):

        status.write("🔍 Retrieving Context...")
        progress.progress(10)

        result = run_code_assistant_pipeline(query)

        progress.progress(100)

    st.success("Analysis Complete!")

    st.divider()

    # Context
    with st.expander("📚 Retrieved Context", expanded=False):
        st.code(result["context"])

    # User Agent
    with st.expander("👤 User Agent"):
        st.write(result["user_responses"])

    # Research Agent
    with st.expander("🔬 Research Agent"):
        st.write(result["research_responses"])

    # Bug Agent
    with st.expander("🐞 Bug Detection Agent"):
        st.write(result["bug_responses"])

    # Optimization Agent
    with st.expander("⚡ Optimization Agent"):
        st.write(result["optimization_responses"])

    # Documentation Agent
    with st.expander("📖 Documentation Agent"):
        st.write(result["documentation_responses"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Final Report")
        st.write(result["report"])

    with col2:
        st.subheader("🎯 Critic Feedback")
        st.write(result["feedback"])

    st.success("✅ Report saved successfully.")
    
    
    #streamlit run AICodeAssistant/AI_Code_Assistant/app.py