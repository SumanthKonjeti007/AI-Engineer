# Simple Hello Agent using LangGraph
# Basic example of state concatenation

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Simple state structure
class SimpleState(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    greeting: str

# Node 1: Get the name
def get_name(state: SimpleState) -> SimpleState:
    """Get the name from input"""
    # Simple input - just assume name is passed directly
    name = state.get("name", "Friend")
    
    # Concatenate to existing state (not replace!)
    return {
        **state,  # Keep existing state
        "name": name
    }

# Node 2: Create greeting
def create_greeting(state: SimpleState) -> SimpleState:
    """Create hello + name greeting"""
    name = state["name"]
    greeting = f"Hello {name}!"
    
    # Concatenate to existing state (not replace!)
    return {
        **state,  # Keep existing state
        "greeting": greeting
    }

# Create the simple graph
def create_simple_agent():
    workflow = StateGraph(SimpleState)
    
    # Add nodes
    workflow.add_node("get_name", get_name)
    workflow.add_node("create_greeting", create_greeting)
    
    # Simple flow
    workflow.set_entry_point("get_name")
    workflow.add_edge("get_name", "create_greeting")
    workflow.add_edge("create_greeting", END)
    
    return workflow.compile()

# Test it
def test_simple():
    agent = create_simple_agent()
    
    # Simple input
    initial_state = {
        "messages": [],
        "name": "Bob",
        "greeting": ""
    }
    
    result = agent.invoke(initial_state)
    
    print("=== Simple Hello Agent ===")
    print(f"Input name: {initial_state['name']}")
    print(f"Output: {result['greeting']}")
    print(f"Final state: {result}")

if __name__ == "__main__":
    test_simple()

