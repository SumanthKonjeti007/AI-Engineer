# Personalized Compliment Agent using LangGraph
# Exercise for Graph I - State Concatenation

import json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Define the state structure
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    compliments: list
    current_compliment: str

# Node 1: Extract name from input
def extract_name(state: AgentState) -> AgentState:
    """Extract the name from the input and add it to state"""
    # Get the latest message
    latest_message = state["messages"][-1]
    
    # Parse the input to extract name
    try:
        input_data = json.loads(latest_message.content)
        name = input_data.get("name", "Friend")
    except:
        name = "Friend"
    
    # Concatenate to existing state (not replace!)
    return {
        **state,
        "name": name,
        "compliments": state.get("compliments", []) + [f"Name extracted: {name}"]
    }

# Node 2: Generate personalized compliment
def generate_compliment(state: AgentState) -> AgentState:
    """Generate a personalized compliment based on the name"""
    name = state["name"]
    
    # Create a personalized compliment
    compliment = f"{name}, you're doing an amazing job learning LangGraph!"
    
    # Concatenate to existing state (not replace!)
    return {
        **state,
        "current_compliment": compliment,
        "compliments": state.get("compliments", []) + [f"Compliment generated: {compliment}"]
    }

# Node 3: Format final output
def format_output(state: AgentState) -> AgentState:
    """Format the final output with the compliment"""
    compliment = state["current_compliment"]
    
    # Add the final output to messages
    final_message = {
        "role": "assistant",
        "content": compliment
    }
    
    # Concatenate to existing state (not replace!)
    return {
        **state,
        "messages": state["messages"] + [final_message],
        "compliments": state.get("compliments", []) + [f"Output formatted: {compliment}"]
    }

# Create the graph
def create_compliment_agent():
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("extract_name", extract_name)
    workflow.add_node("generate_compliment", generate_compliment)
    workflow.add_node("format_output", format_output)
    
    # Define the flow
    workflow.set_entry_point("extract_name")
    workflow.add_edge("extract_name", "generate_compliment")
    workflow.add_edge("generate_compliment", "format_output")
    workflow.add_edge("format_output", END)
    
    # Compile the graph
    return workflow.compile(checkpointer=MemorySaver())

# Test the agent
def test_agent():
    # Create the agent
    agent = create_compliment_agent()
    
    # Test input
    test_input = {"name": "Bob"}
    
    # Initialize state
    initial_state = {
        "messages": [{"role": "user", "content": json.dumps(test_input)}],
        "name": "",
        "compliments": [],
        "current_compliment": ""
    }
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    print("=== Personalized Compliment Agent Test ===")
    print(f"Input: {test_input}")
    print(f"Output: {result['current_compliment']}")
    print(f"\nState History (showing concatenation):")
    for i, compliment in enumerate(result['compliments'], 1):
        print(f"{i}. {compliment}")
    
    return result

# Test with multiple names
def test_multiple_names():
    agent = create_compliment_agent()
    
    test_names = ["Alice", "Charlie", "Diana"]
    
    for name in test_names:
        test_input = {"name": name}
        
        initial_state = {
            "messages": [{"role": "user", "content": json.dumps(test_input)}],
            "name": "",
            "compliments": [],
            "current_compliment": ""
        }
        
        result = agent.invoke(initial_state)
        print(f"\n{name}: {result['current_compliment']}")

if __name__ == "__main__":
    # Run the main test
    test_result = test_agent()
    
    print("\n" + "="*50)
    print("Testing with multiple names:")
    test_multiple_names()

