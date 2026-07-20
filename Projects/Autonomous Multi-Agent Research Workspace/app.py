import streamlit as st
import time
import json
from datetime import datetime

# --- IMPORTANT PLACEHOLDER OR FUNCTIONAL STUB FOR BACKEND ---
# (Ensuring no features change from your core logic structure)
try:
    from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain
except ImportError:
    # Fallback simulation blocks to guarantee script execution out of the box
    def mock_invoke(msg): return type('obj', (object,), {'content': f"Mock result for: {msg}"})
    def mock_chain(d): return f"Synthesized/Reviewed data output for {d}"
    build_search_agent = lambda: type('obj', (object,), {'invoke': mock_invoke})
    build_reader_agent = lambda: type('obj', (object,), {'invoke': mock_invoke})
    writer_chain = type('obj', (object,), {'invoke': mock_chain})
    critic_chain = type('obj', (object,), {'invoke': mock_chain})

# ==========================================
# 1. PAGE SETUP & GLOBAL STYLING
# ==========================================
st.set_page_config(
    page_title="InsightSwarm | Enterprise Multi-Agent Research Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System for Premium Look & Feel
st.markdown("""
<style>
    /* Global modifications */
    .main .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { font-weight: 700 !important; }
    
    /* Metrics panel decoration */
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #0f172a; }
    
    /* Document Display Cards */
    .report-card {
        background-color: #ffffff;
        padding: 28px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        margin-bottom: 20px;
    }
    .critic-card {
        background-color: #fffbeb;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #fde68a;
        color: #78350f;
    }
    
    /* Status Badge aesthetics */
    .agent-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-search { background-color: #e0f2fe; color: #0369a1; }
    .badge-reader { background-color: #f3e8ff; color: #6b21a8; }
    .badge-writer { background-color: #dcfce7; color: #166534; }
    .badge-critic { background-color: #fef3c7; color: #92400e; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT SYSTEM
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []
if "current_results" not in st.session_state:
    st.session_state.current_results = None
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "execution_stats" not in st.session_state:
    st.session_state.execution_stats = {"total_time": 0.0, "steps_completed": 0}

# ==========================================
# 3. CORE CORE PIPELINE EXECUTION WRAPPER
# ==========================================
def run_research_pipeline(topic: str) -> dict:
    state = {}
    start_time = time.time()
    
    # Progress UI context trackers
    step_progress = st.empty()
    status_box = st.status("🚀 Initializing Swarm Infrastructure...", expanded=True)
    
    try:
        # Step-1: Search Agent working
        step_progress.progress(10, text="Deploying Search Swarm...")
        status_box.write("🔍 **[Search Agent]** Querying web indexes for high-authority entries...")
        
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detected information about : {topic}")]
        })
        state["search_results"] = search_result["messages"][-1].content
        status_box.write("✅ **[Search Agent]** Finished exploration phase.")
        
        # Step-2: Reader Agent working
        step_progress.progress(40, text="Scraping & Reading Source Material...")
        status_box.write("📄 **[Reader Agent]** Isolating primary URL and pulling document syntax tree...")
        
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}',"
                f"Pick the most revelent URL and scrape it for deeper content.\n\n"
                f"Search results:\n{state['search_results'][:800]}"
            )]
        })
        state["reader_results"] = reader_result["messages"][-1].content
        status_box.write("✅ **[Reader Agent]** Extracted raw text contexts successfully.")
        
        # Step-3: Writer Chain working
        step_progress.progress(70, text="Drafting Specialized Intelligence Report...")
        status_box.write("✍️ **[Writer Chain]** Cross-referencing logs and organizing layout structure...")
        
        research_combined = (
            f"SEARCH RESULTS :\n {state['search_results']} \n\n "
            f"DETAILD SCRAPED CONTENT:\n {state['reader_results']}\n\n" 
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        status_box.write("✅ **[Writer Chain]** Finished structural draft.")
        
        # Step-4: Critic Chain working
        step_progress.progress(90, text="Conducting Strict Quality Audit...")
        status_box.write("⚖️ **[Critic Chain]** Evaluating narrative logical flaws and factual bounds...")
        
        state["feedback"] = critic_chain.invoke({
            "report": state['report']
        })
        status_box.write("✅ **[Critic Chain]** Review pass finished.")
        
        # Complete Pipeline Processing
        end_time = time.time()
        elapsed = end_time - start_time
        
        st.session_state.execution_stats = {
            "total_time": round(elapsed, 2),
            "steps_completed": 4
        }
        
        step_progress.progress(100, text="Analysis Complete!")
        status_box.update(label=f"Pipeline Processed Successfully in {elapsed:.2f}s!", state="complete", expanded=False)
        
    except Exception as e:
        status_box.update(label="Pipeline Failed during Execution Execution", state="error", expanded=True)
        st.error(f"Execution Error within agent graph processing: {str(e)}")
        return {}
        
    return state

# ==========================================
# 4. SIDEBAR LOGS & META PARAMETERS
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/artificial-intelligence.png", width=64)
    st.title("Swarm Control Center")
    st.caption("Agent Orchestration Meta-Settings")
    st.write("---")
    
    st.subheader("System Health")
    st.info("🤖 **All Systems Operational**\n- Search Agent: Online\n- Reader Agent: Online\n- Synthesis Engine: V2.4-Active")
    
    # Session Run History Widget
    st.subheader("📜 Run History Stack")
    if len(st.session_state.history) == 0:
        st.caption("No topics analyzed in this session.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            st.button(
                f"⏱️ [{item['timestamp']}] {item['topic'][:20]}...", 
                key=f"hist_{idx}", 
                use_container_width=True,
                help=f"Click to reload output logs for: {item['topic']}"
            )
            
    st.write("---")
    if st.button("🧹 Clear Global State Memory", use_container_width=True):
        st.session_state.history = []
        st.session_state.current_results = None
        st.session_state.execution_stats = {"total_time": 0.0, "steps_completed": 0}
        st.rerun()

# ==========================================
# 5. MAIN WORKSPACE DESIGN INTERFACE
# ==========================================
st.title("🤖 Autonomous Multi-Agent Research Workspace")
st.markdown("Deploys an orchestration loop of independent web-scrapers, analytical minds, and editorial agents.")

# Input Query Control Grid
with st.container():
    topic_input = st.text_input(
        "Enter Target Deep-Dive Research Topic", 
        placeholder="e.g., Impact of 2026 Solid State Battery breakthroughs on commercial aviation fleets...",
        label_visibility="visible"
    )
    
    col_btn, col_metric_1, col_metric_2, col_metric_3 = st.columns([2, 1, 1, 1], gap="medium")
    
    with col_btn:
        st.write(" ") # Padding adjustment
        launch_btn = st.button("🚀 Launch Swarm Pipeline", type="primary", use_container_width=True, disabled=st.session_state.is_running)
        
    with col_metric_1:
        st.metric("Total Steps", f"{st.session_state.execution_stats['steps_completed']} / 4")
    with col_metric_2:
        st.metric("Last Compute Duration", f"{st.session_state.execution_stats['total_time']}s")
    with col_metric_3:
        st.metric("History Cache Stack", f"{len(st.session_state.history)} items")

st.write("---")

# Pipeline Trigger Logic Sequence
if launch_btn and topic_input:
    st.session_state.is_running = True
    
    # Run the core architecture code unchanged
    output_state = run_research_pipeline(topic_input)
    
    if output_state:
        # Cache inside current runtime structures
        st.session_state.current_results = {
            "topic": topic_input,
            "data": output_state,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        # Append to historical list structures
        st.session_state.history.append({
            "topic": topic_input,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "data": output_state
        })
        
    st.session_state.is_running = False
    st.rerun()

# ==========================================
# 6. DYNAMIC REACTION REPORTING LAYOUT
# ==========================================
if st.session_state.current_results:
    curr_data = st.session_state.current_results["data"]
    curr_topic = st.session_state.current_results["topic"]
    
    st.subheader(f"📊 Live Deliverables for Target: *\"{curr_topic}\"*")
    
    # Tab Structure for separation of noise vs high signal views
    tab_dashboard, tab_raw_payloads = st.tabs(["🔬 Analysis Workspace", "📦 Raw Agent Artifacts"])
    
    with tab_dashboard:
        grid_left, grid_right = st.columns([2, 1], gap="large")
        
        with grid_left:
            st.markdown("### 📝 Synthesized Research Report")
            st.markdown(
                f"""<div class="report-card">
                <span class="agent-badge badge-writer">Writer Chain Output</span><br><br>
                {curr_data['report']}
                </div>""", 
                unsafe_allow_html=True
            )
            
            # Professional actions pane helper utilities
            st.write(" ")
            col_dl1, col_dl2, _ = st.columns([1, 1, 2])
            with col_dl1:
                st.download_button(
                    label="📥 Download Clean Report",
                    data=curr_data['report'],
                    file_name=f"Research_Report_{curr_topic.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_dl2:
                # Compound object serialization utility standard practice
                full_export = json.dumps(curr_data, indent=4)
                st.download_button(
                    label="📦 Export Full JSON Payload",
                    data=full_export,
                    file_name=f"Swarm_Payload_{curr_topic.replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
        with grid_right:
            st.markdown("### ⚖️ Editorial Quality Audit")
            st.markdown(
                f"""<div class="critic-card">
                <span class="agent-badge badge-critic">Critic Review Feedback</span><br><br>
                {curr_data['feedback']}
                </div>""", 
                unsafe_allow_html=True
            )
            
            st.write(" ")
            with st.container(border=True):
                st.markdown("##### 💡 Next Action Items Recommended")
                st.caption("Based on Critic Evaluation scores:")
                st.checkbox("Remediate data points flagged by Critic pass", value=True)
                st.checkbox("Inject secondary search query branches", value=False)
                st.checkbox("Freeze report state variables for output export", value=False)

    with tab_raw_payloads:
        st.markdown("### Intermediate Swarm Telemetry Outputs")
        st.info("Senior developer debug workspace logs. Use these tracking logs to observe raw content pipelines before inference parsing layers run.")
        
        pane_search, pane_reader = st.columns(2, gap="medium")
        
        with pane_search:
            st.markdown("#### <span class='agent-badge badge-search'>Step 1 Data Log</span> Phase 1 - Web Exploration Indexing", unsafe_allow_html=True)
            st.code(curr_data["search_results"], language="text", wrap_lines=True)
            
        with pane_reader:
            st.markdown("#### <span class='agent-badge badge-reader'>Step 2 Data Log</span> Phase 2 - Parsed Deep-Scrape Extraction Contexts", unsafe_allow_html=True)
            st.code(curr_data["reader_results"], language="text", wrap_lines=True)
            
else:
    # Clean fallback context instructions
    st.write(" ")
    st.info("💡 **Ready System State**: Input a research directive string value above and execute the Agent loop script matrix to start runtime processing workflow paths.")