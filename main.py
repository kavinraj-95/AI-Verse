import streamlit as st
from graph import app
from agents.profiler import profiler_agent
from agents.market_analyst import market_analyst_agent
from agents.roadmap_planner import roadmap_planner_agent
from agents.executive_agent import executive_agent
from agents.critic_reflector import critic_reflector_agent
import io
import os

st.set_page_config(layout="wide")

st.title("AI-Verse: Your Agentic Career Development Assistant")

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


# Sidebar for user input
with st.sidebar:
    st.header("API Keys")
    st.session_state.google_api_key = st.text_input("Google API Key", type="password")
    st.session_state.reddit_client_id = st.text_input("Reddit Client ID", type="password")
    st.session_state.reddit_client_secret = st.text_input("Reddit Client Secret", type="password")
    st.session_state.reddit_user_agent = st.text_input("Reddit User Agent")

    st.header("Your Profile")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    
    # Disable the button if keys are missing
    all_keys_provided = all([
        st.session_state.google_api_key,
        st.session_state.reddit_client_id,
        st.session_state.reddit_client_secret,
        st.session_state.reddit_user_agent
    ])

    if uploaded_file and st.button("Start Analysis", disabled=not all_keys_provided):
        # Set environment variables for the agents
        os.environ["GOOGLE_API_KEY"] = st.session_state.google_api_key
        os.environ["REDDIT_CLIENT_ID"] = st.session_state.reddit_client_id
        os.environ["REDDIT_CLIENT_SECRET"] = st.session_state.reddit_client_secret
        os.environ["REDDIT_USER_AGENT"] = st.session_state.reddit_user_agent
        
        with st.spinner("Analyzing your profile..."):
            file_contents = uploaded_file.getvalue()
            bytes_io = io.BytesIO(file_contents)
            
            st.session_state.agent_logs.append("Profiler is running...")
            profile = profiler_agent(bytes_io)
            st.session_state.user_profile = profile
            st.session_state.agent_logs.append("Profiler finished.")
            
            st.session_state.agent_logs.append("Market Analyst is running...")
            opportunities = market_analyst_agent(st.session_state.user_profile)
            st.session_state.opportunities = opportunities
            st.session_state.agent_logs.append("Market Analyst finished.")
            
            st.session_state.agent_logs.append("Roadmap Planner is running...")
            roadmap = roadmap_planner_agent(st.session_state.user_profile, st.session_state.opportunities)
            st.session_state.roadmap = roadmap
            st.session_state.agent_logs.append("Roadmap Planner finished.")

            st.session_state.agent_logs.append("Executive Agent is running...")
            if st.session_state.opportunities:
                executive_agent(st.session_state.user_profile, st.session_state.opportunities[0])
            st.session_state.agent_logs.append("Executive Agent finished.")
            st.rerun()

# Main canvas
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Live Thinking Stream")
    log_container = st.container(height=300)
    for log in st.session_state.agent_logs:
        log_container.write(log)

with col2:
    st.header("The Roadmap")
    st.markdown(st.session_state.roadmap)

with col3:
    st.header("Opportunity Feed")
    if st.session_state.opportunities:
        for op in st.session_state.opportunities:
            with st.expander(op.get('title', 'N/A')):
                st.write(f"**Subreddit:** {op.get('subreddit', 'N/A')}")
                st.write(f"**Score:** {op.get('score', 'N/A')}")
                st.markdown(op.get('selftext', ''))
                st.link_button("Go to post", op.get('url', ''))


# Feedback loop simulation
st.header("Simulate Feedback")
rejection_feedback = st.text_input("Enter simulated rejection feedback:")
if st.button("Run Critic Reflector"):
    if rejection_feedback:
        if all_keys_provided:
            with st.spinner("Reflecting on feedback..."):
                os.environ["GOOGLE_API_KEY"] = st.session_state.google_api_key
                
                st.session_state.agent_logs.append("Critic Reflector is running...")
                
                priority_gap = critic_reflector_agent(rejection_feedback)
                st.session_state.agent_logs.append(f"New priority gap identified: {priority_gap}")

                if st.session_state.user_profile:
                    updated_skills = st.session_state.user_profile.get('skills', []) + [priority_gap]
                    st.session_state.user_profile['skills'] = list(set(updated_skills))
                    
                    st.session_state.agent_logs.append("Re-running analysis with new insights...")

                    opportunities = market_analyst_agent(st.session_state.user_profile)
                    st.session_state.opportunities = opportunities
                    
                    roadmap = roadmap_planner_agent(st.session_state.user_profile, st.session_state.opportunities)
                    st.session_state.roadmap = roadmap
                    st.rerun()
        else:
            st.warning("Please provide all API keys before running the reflector.")

    else:
        st.warning("Please enter some feedback.")