import streamlit as st
from graph import app
import io
import os
from langgraph.checkpoint.memory import MemorySaver
import time

st.set_page_config(
    layout="wide",
    page_title="AI-Verse | Agentic Career Assistant",
    page_icon="🚀"
)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("frontend/style.css")

# Header with gradient
st.markdown("""
    <div class="main-header">
        <h1>🚀 AI-VERSE</h1>
        <p class="subtitle">Your Agentic Career Development Assistant</p>
        <div class="status-badge">
            <span class="status-indicator"></span>
            <span>SYSTEM ONLINE</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_logs' not in st.session_state:
    st.session_state.agent_logs = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'opportunities' not in st.session_state:
    st.session_state.opportunities = []
if 'roadmap' not in st.session_state:
    st.session_state.roadmap = ""
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = ""
if 'reddit_client_id' not in st.session_state:
    st.session_state.reddit_client_id = ""
if 'reddit_client_secret' not in st.session_state:
    st.session_state.reddit_client_secret = ""
if 'reddit_user_agent' not in st.session_state:
    st.session_state.reddit_user_agent = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'feedback_loop_count' not in st.session_state:
    st.session_state.feedback_loop_count = 0

# Sidebar for user input
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ CONFIGURATION</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">🔐 API CREDENTIALS</p>', unsafe_allow_html=True)
    st.session_state.google_api_key = st.text_input("Google API Key", type="password", key="google_key")
    st.session_state.reddit_client_id = st.text_input("Reddit Client ID", type="password", key="reddit_id")
    st.session_state.reddit_client_secret = st.text_input("Reddit Client Secret", type="password", key="reddit_secret")
    st.session_state.reddit_user_agent = st.text_input("Reddit User Agent", key="reddit_agent")
    st.markdown('</div>', unsafe_allow_html=True)

    all_keys_provided = all([
        st.session_state.google_api_key,
        st.session_state.reddit_client_id,
        st.session_state.reddit_client_secret,
        st.session_state.reddit_user_agent
    ])

    # API Status indicator
    if all_keys_provided:
        st.markdown('<div class="api-status api-ready">✓ All APIs Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status api-pending">⚠ APIs Required</div>', unsafe_allow_html=True)

    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">📄 RESUME UPLOAD</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf", key="resume_upload")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        st.markdown('<div class="file-uploaded">✓ Resume Loaded</div>', unsafe_allow_html=True)

    st.markdown('<div class="action-section">', unsafe_allow_html=True)
    if st.button("🚀 INITIALIZE ANALYSIS", disabled=not all_keys_provided or not uploaded_file, key="start_btn", use_container_width=True):
        st.session_state.processing = True
        os.environ["GOOGLE_API_KEY"] = st.session_state.google_api_key
        os.environ["REDDIT_CLIENT_ID"] = st.session_state.reddit_client_id
        os.environ["REDDIT_CLIENT_SECRET"] = st.session_state.reddit_client_secret
        os.environ["REDDIT_USER_AGENT"] = st.session_state.reddit_user_agent

        file_contents = uploaded_file.getvalue()
        bytes_io = io.BytesIO(file_contents)

        initial_state = {
            "file_content": bytes_io,
            "agent_logs": [],
            "feedback_loop_count": 0
        }
        
        config = {"configurable": {"thread_id": "1"}}

        # Placeholders for dynamic content
        log_container = st.empty()
        roadmap_container = st.empty()
        opportunities_container = st.empty()

        with st.spinner('🔄 Agents Processing...'):
            for event in app.stream(initial_state, config=config):
                if "agent_logs" in event:
                    st.session_state.agent_logs = event.get('agent_logs', [])

                if 'user_profile' in event:
                    st.session_state.user_profile = event['user_profile']
                
                if 'roadmap' in event:
                    st.session_state.roadmap = event['roadmap']

                if 'opportunities' in event:
                    st.session_state.opportunities = event['opportunities']
        
        st.session_state.processing = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Agent Status Panel
    st.markdown('<div class="agent-status-panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">🤖 AGENT STATUS</p>', unsafe_allow_html=True)
    
    agents = [
        ("Profiler", "👤", st.session_state.user_profile is not None),
        ("Market Analyst", "📊", len(st.session_state.opportunities) > 0),
        ("Roadmap Planner", "🗺️", st.session_state.roadmap != ""),
        ("Executive", "⚡", st.session_state.processing),
        ("Critic Reflector", "🔍", st.session_state.feedback_loop_count > 0)
    ]
    
    for agent_name, icon, is_active in agents:
        status = "agent-active" if is_active else "agent-inactive"
        st.markdown(f'<div class="agent-item {status}">{icon} {agent_name}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main canvas
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="panel-header">🧠 NEURAL STREAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="log-container">', unsafe_allow_html=True)
    
    if st.session_state.agent_logs:
        for log in st.session_state.agent_logs[-20:]:  # Show last 20 logs
            if "starting" in log.lower():
                st.markdown(f'<div class="log-entry log-start">{log}</div>', unsafe_allow_html=True)
            elif "finished" in log.lower() or "identified" in log.lower():
                st.markdown(f'<div class="log-entry log-success">{log}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="log-entry">{log}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="log-entry log-waiting">⏳ Awaiting initialization...</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Profile Summary Card
    if st.session_state.user_profile:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">👤 PROFILE SYNOPSIS</p>', unsafe_allow_html=True)
        
        profile = st.session_state.user_profile
        
        if 'name' in profile:
            st.markdown(f'<p class="profile-field"><strong>Name:</strong> {profile["name"]}</p>', unsafe_allow_html=True)
        
        if 'skills' in profile and profile['skills']:
            skills_html = ', '.join([f'<span class="skill-tag">{skill}</span>' for skill in profile['skills'][:5]])
            st.markdown(f'<p class="profile-field"><strong>Core Skills:</strong><br>{skills_html}</p>', unsafe_allow_html=True)
        
        if 'experience' in profile:
            st.markdown(f'<p class="profile-field"><strong>Experience:</strong> {profile.get("experience", "N/A")}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    tab1, tab2 = st.tabs(["🗺️ THE ROADMAP", "🎯 OPPORTUNITY FEED"])
    
    with tab1:
        if st.session_state.roadmap:
            st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)
            st.markdown(st.session_state.roadmap)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state">', unsafe_allow_html=True)
            st.markdown('### 🗺️ Roadmap Generation Pending')
            st.markdown('Upload your resume and start the analysis to generate your personalized career roadmap.')
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        if st.session_state.opportunities:
            st.markdown(f'<div class="opportunity-count">{len(st.session_state.opportunities)} Opportunities Detected</div>', unsafe_allow_html=True)
            
            for idx, op in enumerate(st.session_state.opportunities):
                with st.expander(f"🎯 {op.get('title', 'Opportunity')}", expanded=(idx == 0)):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.markdown(f"**📍 Subreddit:** r/{op.get('subreddit', 'N/A')}")
                        st.markdown(f"**⭐ Score:** {op.get('score', 'N/A')}")
                    
                    with col_b:
                        if op.get('url'):
                            st.link_button("VIEW POST →", op.get('url', ''), use_container_width=True)
                    
                    if op.get('selftext'):
                        st.markdown("---")
                        st.markdown(op.get('selftext', '')[:500] + "..." if len(op.get('selftext', '')) > 500 else op.get('selftext', ''))
        else:
            st.markdown('<div class="empty-state">', unsafe_allow_html=True)
            st.markdown('### 🎯 Scanning for Opportunities')
            st.markdown('Market analysis will populate relevant opportunities based on your profile.')
            st.markdown('</div>', unsafe_allow_html=True)

# Feedback loop simulation
st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
st.markdown('<div class="panel-header">🔄 ADAPTIVE LEARNING MODULE</div>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns([3, 1])

with col_f1:
    rejection_feedback = st.text_input(
        "Simulate rejection feedback to trigger adaptive learning:",
        placeholder="e.g., Candidate lacks experience in cloud infrastructure...",
        key="feedback_input"
    )

with col_f2:
    st.markdown('<div class="feedback-button-container">', unsafe_allow_html=True)
    run_critic = st.button("🔍 ANALYZE", key="critic_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if run_critic:
    if rejection_feedback:
        if all_keys_provided and st.session_state.user_profile:
            os.environ["GOOGLE_API_KEY"] = st.session_state.google_api_key
            
            initial_state = {
                "rejection_feedback": rejection_feedback,
                "user_profile": st.session_state.user_profile,
                "agent_logs": st.session_state.agent_logs,
                "feedback_loop_count": st.session_state.feedback_loop_count
            }
            
            config = {"configurable": {"thread_id": "1"}}

            with st.spinner('🔄 Critic Reflector Analyzing...'):
                for event in app.stream(initial_state, config=config):
                    if "agent_logs" in event:
                        st.session_state.agent_logs = event.get('agent_logs', [])

                    if 'user_profile' in event:
                        st.session_state.user_profile = event['user_profile']
                    
                    if 'roadmap' in event:
                        st.session_state.roadmap = event['roadmap']

                    if 'opportunities' in event:
                        st.session_state.opportunities = event['opportunities']
                    
                    if 'feedback_loop_count' in event:
                        st.session_state.feedback_loop_count = event['feedback_loop_count']
            
            st.success("✓ Adaptive learning cycle completed!")
            time.sleep(1)
            st.rerun()

        elif not st.session_state.user_profile:
            st.warning("⚠ Please run the initial analysis first.")
        else:
            st.warning("⚠ Please provide all API keys before running the reflector.")
    else:
        st.warning("⚠ Please enter feedback to analyze.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>AI-Verse v2.0 | Powered by Multi-Agent Architecture | Built with LangGraph</p>
    </div>
""", unsafe_allow_html=True)