import io
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import functools
from agents.profiler import profiler_agent
from agents.market_analyst import market_analyst_agent
from agents.roadmap_planner import roadmap_planner_agent
from agents.executive_agent import executive_agent
from agents.critic_reflector import critic_reflector_agent

class GraphState(TypedDict):
    user_profile: dict
    opportunities: List[dict]
    roadmap: str
    feedback_loop_count: int
    agent_logs: List[str]
    priority_gap: str  # Added for the feedback loop
    file_content: io.BytesIO
    rejection_feedback: str

def profiler_node(state: GraphState):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Profiler starting..."]
    user_profile = profiler_agent(state['file_content'])
    return {"user_profile": user_profile, "agent_logs": state['agent_logs']}

def market_analyst_node(state: GraphState):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Market Analyst starting..."]
    opportunities = market_analyst_agent(state['user_profile'])
    return {"opportunities": opportunities, "agent_logs": state['agent_logs']}

def roadmap_planner_node(state: GraphState):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Roadmap Planner starting..."]
    roadmap = roadmap_planner_agent(state['user_profile'], state['opportunities'])
    return {"roadmap": roadmap, "agent_logs": state['agent_logs']}

def executive_agent_node(state: GraphState):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Executive Agent starting..."]
    # For now, we'll just take the first opportunity
    if state['opportunities']:
        executive_agent(state['user_profile'], state['opportunities'][0])
    return {"agent_logs": state.get('agent_logs', []) + ["Agent: Executive Agent finished."]}


def critic_reflector_node(state: GraphState):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Critic Reflector starting..."]
    priority_gap = critic_reflector_agent(state['rejection_feedback'])
    
    # Update user profile to reflect the new gap
    updated_skills = state['user_profile'].get('skills', []) + [priority_gap]
    state['user_profile']['skills'] = list(set(updated_skills)) # remove duplicates
    
    return {
        "priority_gap": priority_gap,
        "user_profile": state['user_profile'],
        "feedback_loop_count": state.get('feedback_loop_count', 0) + 1,
        "agent_logs": state.get('agent_logs', []) + [f"New priority gap identified: {priority_gap}"]
    }

def entry_point_router(state: GraphState):
    if state.get("rejection_feedback"):
        return "critic_reflector"
    return "profiler"

def should_loop(state: GraphState):
    return state.get("feedback_loop_count", 0) < 3 # Limit loops to 3 for now

# Define the graph
workflow = StateGraph(GraphState)

workflow.add_node("profiler", profiler_node)
workflow.add_node("market_analyst", market_analyst_node)
workflow.add_node("roadmap_planner", roadmap_planner_node)
workflow.add_node("executive_agent", executive_agent_node)
workflow.add_node("critic_reflector", critic_reflector_node)


# Set the entrypoint
workflow.set_conditional_entry_point(
    entry_point_router,
    {
        "profiler": "profiler",
        "critic_reflector": "critic_reflector",
    },
)

# Add edges
workflow.add_edge("profiler", "market_analyst")
workflow.add_edge("critic_reflector", "market_analyst")
workflow.add_edge("market_analyst", "roadmap_planner")
workflow.add_edge("roadmap_planner", "executive_agent")

# The feedback loop
workflow.add_conditional_edges(
    "executive_agent",
    should_loop,
    {
        True: "market_analyst", # Loop back to market_analyst
        False: END
    }
)
# This is a simplified loop condition. In a real scenario, the critic would be a separate entry point.

# Compile the graph
app = workflow.compile()
