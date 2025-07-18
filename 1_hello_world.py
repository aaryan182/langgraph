# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with a single field called 'message' of type str
class AgentState(TypedDict):
    # The 'message' field is a string that will be used to store a message in the state
    message: str

# Define a function called greeting_node, which takes an AgentState as input and returns a new AgentState
def greeting_node(state: AgentState) -> AgentState:
    # This function is a node in the state graph that adds a greeting message to the state
    """Simple node that adds a greeting message to the state"""
    
    # Access the 'message' field of the input state and append a greeting message to it
    # The greeting message is constructed by concatenating "Hey", the original message, and ", how is your day?"
    state['message'] = "Hey" + state["message"] + ", how is your day?"
    
    # Return the modified state
    return state

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called "greeter", which is implemented by the greeting_node function
graph.add_node("greeter", greeting_node)

# Set the entry point of the graph to the "greeter" node, which means that this node will be executed first
graph.set_entry_point("greeter")

# Set the finish point of the graph to the "greeter" node which means that this node will be executed last
graph.set_finish_point("greeter")

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application, passing in an initial state with a message field set to "aaryan"
result = app.invoke({"message": "aaryan"})

# Access the modified message field of the resulting state and print it
result["message"]