import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Research System")
st.caption("Search Agent → Reader Agent → Writer → Critic")

st.markdown("---")

topic = st.text_input(
    "Research Topic",
    placeholder="Example: Artificial Intelligence in Healthcare"
)

if st.button("🚀 Generate Research Report", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("🔎 Search Agent is finding information..."):
        state = run_research_pipeline(topic)

    st.success("Research Completed!")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔍 Search Results",
            "📖 Reader",
            "📝 Report",
            "⭐ Critic"
        ]
    )

    with tab1:
        st.subheader("Search Agent Output")
        st.write(state["search_results"])

    with tab2:
        st.subheader("Reader Agent Output")
        st.write(state["reader_results"])

    with tab3:
        st.subheader("Research Report")

        st.markdown(state["report"])

        st.download_button(
            "⬇ Download Report",
            state["report"],
            file_name=f"{topic.replace(' ','_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with tab4:
        st.subheader("Critic Feedback")
        st.write(state["feedback"])