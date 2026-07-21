import os
import sys
import time
import glob
import tempfile

import streamlit as st

# Ensures Python adds the workspace root to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PY.agents import (
    build_eda_agent,
    build_visualization_agent,
    build_correlation_agent,
    writer_chain,
    critic_chain,
)

# ************************
# Page config
# ************************
st.set_page_config(
    page_title="CSV Insight Pipeline",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ************************
# Responsive styling
# ************************
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }
        .step-card {
            padding: 0.9rem 1.1rem;
            border-radius: 10px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 0.6rem;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        @media (max-width: 640px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ************************
# Session state
# ************************
if "pipeline_state" not in st.session_state:
    st.session_state.pipeline_state = None
if "running" not in st.session_state:
    st.session_state.running = False

# ************************
# Sidebar
# ************************
with st.sidebar:
    st.title("📊 CSV Insight Pipeline")
    st.caption("EDA → Visualization → Correlation → Report → Critic")
    st.divider()
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    st.divider()
    st.markdown(
        "**Pipeline steps**\n"
        "1. EDA Agent\n"
        "2. Visualization Agent\n"
        "3. Correlation Agent\n"
        "4. Writer Chain (Report)\n"
        "5. Critic Chain (Feedback)"
    )

# ************************
# Main area
# ************************
st.title("CSV Analysis Pipeline")
st.write(
    "Upload a CSV file in the sidebar, then run the pipeline to get an "
    "automated EDA, visualizations, correlation analysis, a written report, "
    "and critic feedback."
)

run_col, clear_col = st.columns([1, 1])
run_clicked = run_col.button(
    "▶ Run Pipeline", type="primary", use_container_width=True,
    disabled=(uploaded_file is None) or st.session_state.running,
)
clear_clicked = clear_col.button(
    "🗑 Clear Results", use_container_width=True,
    disabled=st.session_state.running,
)

if clear_clicked:
    st.session_state.pipeline_state = None
    st.rerun()

if uploaded_file is None:
    st.info("Upload a CSV file from the sidebar to get started.")


def run_csv_pipeline_ui(csv_path: str) -> dict:
    """Same logic as pipeline.run_csv_pipeline, but reporting progress to the UI."""
    state = {}

    status = st.status("Running pipeline...", expanded=True)

    # Step 1 - EDA agent
    status.write("**Step 1 — EDA Agent is working**")
    eda_agent = build_eda_agent()
    eda_result = eda_agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze the CSV file located at: {csv_path}"}]
    })
    state['eda_results'] = eda_result['messages'][-1].content
    status.write("✅ EDA Agent finished")
    time.sleep(2)

    # Step 2 - Visualization agent
    status.write("**Step 2 — Visualization Agent is working**")
    viz_agent = build_visualization_agent()
    viz_result = viz_agent.invoke({
        "messages": [{"role": "user", "content": f"Generate visualizations for the CSV file at: {csv_path}"}]
    })
    state['viz_results'] = viz_result['messages'][-1].content
    status.write("✅ Visualization Agent finished")
    time.sleep(2)

    # Step 3 - Correlation agent
    status.write("**Step 3 — Correlation Agent is working**")
    cor_agent = build_correlation_agent()
    cor_result = cor_agent.invoke({
        "messages": [{"role": "user", "content": f"Perform correlation analysis on the CSV file at: {csv_path}"}]
    })
    state['cor_results'] = cor_result['messages'][-1].content
    status.write("✅ Correlation Agent finished")
    time.sleep(2)

    # Step 4 - Writer Chain
    status.write("**Step 4 — Writer Chain is working**")
    state['report'] = writer_chain.invoke({
        "eda": state['eda_results'][:2000],
        "visualization": state['viz_results'][:2000],
        "correlation": state['cor_results'][:2000]
    })
    status.write("✅ Writer Chain finished")
    time.sleep(2)

    # Step 5 - Critic agent
    status.write("**Step 5 — Critic Chain is working**")
    state["feedback"] = critic_chain.invoke({
        "report": state['report'][:3000]
    })
    status.write("✅ Critic Chain finished")

    status.update(label="Pipeline complete", state="complete", expanded=False)
    return state


if run_clicked and uploaded_file is not None:
    st.session_state.running = True
    # Persist the uploaded file to disk so the pipeline (which expects a path) can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_f:
        tmp_f.write(uploaded_file.getbuffer())
        tmp_path = tmp_f.name

    try:
        result_state = run_csv_pipeline_ui(tmp_path)
        st.session_state.pipeline_state = result_state
    except Exception as e:
        st.error(f"Pipeline failed: {e}")
    finally:
        st.session_state.running = False
        try:
            os.remove(tmp_path)
        except OSError:
            pass

# ************************
# Results
# ************************
state = st.session_state.pipeline_state
if state:
    st.divider()
    st.header("Results")

    tab_report, tab_feedback, tab_eda, tab_viz, tab_cor = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 EDA", "📈 Visualization", "🔗 Correlation"]
    )

    with tab_report:
        st.subheader("Final Report")
        st.markdown(state.get("report", "_No report generated._"))
        st.download_button(
            "Download report (.txt)",
            data=str(state.get("report", "")),
            file_name="report.txt",
            use_container_width=True,
        )

    with tab_feedback:
        st.subheader("Critic Report Feedback")
        st.markdown(state.get("feedback", "_No feedback generated._"))

    with tab_eda:
        st.subheader("EDA Results")
        st.markdown(state.get("eda_results", "_No EDA results._"))

    with tab_viz:
        st.subheader("Visualization Results")
        st.markdown(state.get("viz_results", "_No visualization results._"))

        plot_files = sorted(glob.glob(os.path.join("plots", "*.png")))
        if plot_files:
            st.markdown("---")
            st.markdown("**Generated Plots**")
            cols = st.columns(2)
            for i, img_path in enumerate(plot_files):
                with cols[i % 2]:
                    st.image(img_path, use_container_width=True, caption=os.path.basename(img_path))
        else:
            st.warning("No plots found in the `plots/` folder.")

    with tab_cor:
        st.subheader("Correlation Results")
        st.markdown(state.get("cor_results", "_No correlation results._"))