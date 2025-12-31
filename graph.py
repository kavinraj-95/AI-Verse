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

# Helper function to add logs
def log_agent_step(func):
    @functools.wraps(func)
    def wrapper(state: GraphState, *args, **kwargs):
        # Call the actual agent function
        result = func(state, *args, **kwargs)
        
        # Get the name of the agent
        agent_name = func.__name__.replace('_agent', '').replace('_node', '')
        
        # Create a log entry
        log_entry = f"Agent: {agent_name.capitalize()} completed."
        
        # Append the log to the agent_logs
        new_logs = state.get('agent_logs', []) + [log_entry]
        
        # The agent function is expected to return a dictionary 
        # that updates the state. We add the logs to that dictionary.
        if isinstance(result, dict):
            result['agent_logs'] = new_logs
        else:
            # If the agent doesn't return a dict, we need to handle it
            # This part might need adjustment based on agent return types
            pass

        return result
    return wrapper

def profiler_node(state: GraphState, file_content):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Profiler starting..."]
    user_profile = profiler_agent(file_content)
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


def critic_reflector_node(state: GraphState, rejection_feedback: str):
    state['agent_logs'] = state.get('agent_logs', []) + ["Agent: Critic Reflector starting..."]
    priority_gap = critic_reflector_agent(rejection_feedback)
    
    # Update user profile to reflect the new gap
    updated_skills = state['user_profile'].get('skills', []) + [priority_gap]
    state['user_profile']['skills'] = list(set(updated_skills)) # remove duplicates
    
    return {
        "priority_gap": priority_gap,
        "user_profile": state['user_profile'],
        "feedback_loop_count": state.get('feedback_loop_count', 0) + 1,
        "agent_logs": state.get('agent_logs', []) + [f"New priority gap identified: {priority_gap}"]
    }

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
workflow.set_entry_point("profiler")

# Add edges
workflow.add_edge("profiler", "market_analyst")
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
