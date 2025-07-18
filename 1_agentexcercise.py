# Import the TypedDict type from the typing module, which is used to define a dictionary with a specific structure
from typing import TypedDict

# Import the StateGraph class from the langgraph.graph module, which is used to define a graph of states
from langgraph.graph import StateGraph

# Define a class called AgentState, which is a TypedDict with a single field called 'message' of type str
class AgentState(TypedDict):
    # The 'message' field is a string that will be used to store a message in the state
    message: str

# Define a function called congrats_node, which takes an AgentState as input and returns a new AgentState
def congrats_node(state: AgentState) -> AgentState:
    # This function is a node in the state graph that adds a congratulations message to the state
    """Simple node that adds a congratulations message to the state"""
    
    # Access the 'message' field of the input state and append a congratulations message to it
    # The congratulations message is constructed by concatenating the original message and a fixed string
    state['message'] = state["message"] + ", you are doing an amazing job learning langgraph"
    
    # Return the modified state
    return state

# Create a new StateGraph instance, passing in the AgentState class as the state type
graph = StateGraph(AgentState)

# Add a new node to the graph, called "congratulations", which is implemented by the congrats_node function
graph.add_node("congratulations", congrats_node)

# Set the entry point of the graph to the "congratulations" node, which means that this node will be executed first
graph.set_entry_point("congratulations")

# Set the finish point of the graph to the "congratulations" node, which means that this node will be executed last
# Since there is only one node in the graph, the entry and finish points are the same
graph.set_finish_point("congratulations")

# Compile the graph into an executable application
app = graph.compile()

# Invoke the application, passing in an initial state with a message field set to "aaryan"
# The application will execute the "congratulations" node with the initial state as input
result = app.invoke({"message": "aaryan"})

# Access the modified message field of the resulting state and print it
# The resulting state will have the original message "aaryan" with the congratulations message appended to it
result["message"]