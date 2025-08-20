# Personalized Compliment Agent with LangGraph

This project implements the **Exercise for Graph I** from the LangGraph Complete Course - creating a Personalized Compliment Agent that demonstrates **state concatenation** (not replacement) as required.

## 🎯 Exercise Requirements

- **Input:** `{"name": "Bob"}`
- **Output:** `"Bob, you're doing an amazing job learning LangGraph!"`
- **Key Requirement:** Concatenate the state, not replace it!

## 🚀 Quick Start

### 1. Set up your virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the agent
```bash
python personalized_compliment_agent.py
```

## 🏗️ Architecture

The agent consists of **3 nodes** that work together:

1. **`extract_name`** - Extracts the name from input JSON
2. **`generate_compliment`** - Creates a personalized compliment
3. **`format_output`** - Formats the final output

## 🔑 Key Implementation Details

### State Concatenation (Not Replacement!)
Each node demonstrates state concatenation:

```python
# Instead of replacing state:
return {"name": name}

# We concatenate to existing state:
return {
    **state,  # Keep all existing state
    "name": name,
    "compliments": state.get("compliments", []) + [f"Name extracted: {name}"]
}
```

### State Structure
```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history
    name: str                                # Extracted name
    compliments: list                        # History of compliments (showing concatenation)
    current_compliment: str                  # Final output
```

## 📊 Expected Output

```
=== Personalized Compliment Agent Test ===
Input: {'name': 'Bob'}
Output: Bob, you're doing an amazing job learning LangGraph!

State History (showing concatenation):
1. Name extracted: Bob
2. Compliment generated: Bob, you're doing an amazing job learning LangGraph!
3. Output formatted: Bob, you're doing an amazing job learning LangGraph!

==================================================
Testing with multiple names:

Alice: Alice, you're doing an amazing job learning LangGraph!

Charlie: Charlie, you're doing an amazing job learning LangGraph!

Diana: Diana, you're doing an amazing job learning LangGraph!
```

## 🧪 Testing

The agent includes built-in tests for:
- Single name input (Bob)
- Multiple names (Alice, Charlie, Diana)
- State concatenation verification

## 🔄 Graph Flow

```
Input → extract_name → generate_compliment → format_output → Output
```

Each node adds to the state without replacing previous information, demonstrating the key concept of state concatenation in LangGraph.

## 📚 Learning Points

- **State Management:** How to properly manage state across nodes
- **Concatenation vs Replacement:** The difference between adding to state vs. overwriting it
- **Node Communication:** How nodes pass information through the graph
- **Error Handling:** Graceful fallbacks for malformed input
- **Testing:** How to verify your LangGraph implementation works correctly

## 🚨 Troubleshooting

If you get import errors:
1. Make sure your virtual environment is activated
2. Check that all dependencies are installed: `pip list | grep lang`
3. Verify Python version: `python --version` (should be 3.8+)

## 🎉 Next Steps

After mastering this exercise, you can:
- Add more personalization (age, interests, etc.)
- Implement conditional logic in nodes
- Add external API calls for dynamic compliments
- Create more complex state structures
- Build multi-turn conversations

